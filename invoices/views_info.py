from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Invoice, Offer, Reminder, Customer


@login_required
@permission_required("invoices_invoices_info")
def ajax_invoice_info(request):
    now = timezone.now()
    data = (
        Invoice.objects
        .filter(issue_date__year=now.year, issue_date__month=now.month)
        .values("status")
        .annotate(count=Count("id"))
    )
    return JsonResponse({item["status"]: item["count"] for item in data})


@login_required
@permission_required("invoices_offers_info")
def ajax_offer_info(request):
    now = timezone.now()
    data = (
        Offer.objects
        .filter(issue_date__year=now.year, issue_date__month=now.month)
        .values("status")
        .annotate(count=Count("id"))
    )
    return JsonResponse({item["status"]: item["count"] for item in data})


@login_required
@permission_required("invoices_reminders_info")
def ajax_reminder_info(request):
    now = timezone.now()
    data = (
        Reminder.objects
        .filter(issue_date__year=now.year, issue_date__month=now.month)
        .values("status")
        .annotate(count=Count("id"))
    )
    return JsonResponse({item["status"]: item["count"] for item in data})


@login_required
@permission_required("invoices_info")
def ajax_kpi_info(request):
    today = timezone.now().date()

    overdue_invoices = Invoice.objects.filter(status="overdue").count()
    open_invoices = Invoice.objects.filter(status="sent").count()
    open_offers = Offer.objects.filter(status="sent").count()
    open_reminders = Reminder.objects.filter(status="sent").count()

    overdue_amount = (
        Invoice.objects
        .filter(status="overdue")
        .aggregate(total=Sum("items__unit_price_net"))["total"] or 0
    )

    return JsonResponse({
        "overdue_invoices": overdue_invoices,
        "open_invoices": open_invoices,
        "open_offers": open_offers,
        "open_reminders": open_reminders,
    })


@login_required
@permission_required("invoices_customers_info")
def ajax_customer_info(request):
    start_of_week = timezone.now().date() - timedelta(days=timezone.now().weekday())
    return JsonResponse({
        "total": Customer.objects.count(),
        "new_this_week": Customer.objects.filter(created_at__date__gte=start_of_week).count(),
        "companies": Customer.objects.filter(customer_type="company").count(),
        "private": Customer.objects.filter(customer_type="private").count(),
    })