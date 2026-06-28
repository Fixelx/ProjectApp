from django.utils import timezone
from .models import Invoice, Offer, Reminder

def mark_overdue():
    today = timezone.now().date()

    Invoice.objects.filter(
        status="sent",
        due_date__lt=today,
    ).update(status="overdue")

    Offer.objects.filter(
        status="sent",
        due_date__lt=today,
    ).update(status="expired")

    Reminder.objects.filter(
        status="sent",
        due_date__lt=today,
    ).update(status="expired")