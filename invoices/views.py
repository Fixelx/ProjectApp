from django.contrib.auth.decorators import login_required
from accounts.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, CustomerContact, CustomerLocation, Item, Invoice, InvoiceItem, Unit, Offer, OfferItem, Reminder, InvoicePaymentAllocation, InvoicePayment
from .forms import CustomerForm, ItemForm, CustomerInvoiceForm, ProjectInvoiceForm, InvoiceItemForm, OfferForm, OfferItemForm, ReminderForm, InvoicePaymentForm
from datetime import date
from projects.models import Project 
from django.http import JsonResponse, FileResponse
from decimal import Decimal
from time_tracking.models import TimeEntry
from finance.models import Expense
from core.models import CompanySetting
from django.views.decorators.http import require_POST
from collections import defaultdict
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.utils import timezone
from weasyprint import HTML
import io
from django.db.models import Prefetch, Sum
from .tables import ItemTable, CustomerTable, CustomerArchivedTable, ReminderTable, InvoiceTable, InvoiceItemTable, OfferTable, OfferItemTable, InvoicePaymentTable
from django_tables2 import RequestConfig
from finance.models import Category, Supplier

def generate_document_number(template, number):
    today = date.today()
    return template.format(
        year=today.strftime("%Y"),
        month=today.strftime("%m"),
        day=today.strftime("%d"),
        number=str(number).zfill(5),
    )

@login_required
@permission_required("invoices_view")
def invoices_overview(request):
    return render(request, "invoices/overview.html")



@login_required
@permission_required("invoices_customers_view")
def customers_overview(request):
    customers = Customer.objects.filter(active=True).order_by("company_name")
    archived_customers = Customer.objects.filter(active=False).order_by("company_name")

    table = CustomerTable(customers)
    RequestConfig(
        request,
        paginate=False
    ).configure(table)

    table_archived = CustomerArchivedTable(archived_customers)
    RequestConfig(
        request,
        paginate=False
    ).configure(table_archived)

    return render(request, "invoices/customers/overview.html", {
        "table": table, "table_archived": table_archived,
    })


@login_required
@permission_required("invoices_customers_add")
def customers_add(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("invoices:customers_overview")

    else:
        form = CustomerForm()

    return render(request, "invoices/customers/add.html", {
        "form": form,
    })



@login_required
@permission_required("invoices_customers_edit")
def customers_edit(request, customer_id):

    customer = get_object_or_404(
        Customer.objects.prefetch_related(
            "contacts",
            "locations",
        ),
        id=customer_id
    )


    if request.method != "POST":
        return redirect(
            "invoices:customers_detail",
            customer.id
        )


    # =========================
    # CUSTOMER SAVE
    # =========================

    form = CustomerForm(
        request.POST,
        instance=customer
    )

    if form.is_valid():
        form.save()



    # =========================
    # CONTACT DELETE
    # =========================

    delete_contact_id = request.POST.get(
        "delete_contact_id"
    )

    if delete_contact_id:

        CustomerContact.objects.filter(
            id=delete_contact_id,
            customer=customer
        ).delete()

        return redirect(
            "invoices:customers_detail",
            customer.id
        )



    # =========================
    # CONTACT UPDATE
    # =========================

    for contact in customer.contacts.all():

        contact.first_name = request.POST.get(
            f"contact_first_name_{contact.id}",
            contact.first_name
        )

        contact.last_name = request.POST.get(
            f"contact_last_name_{contact.id}",
            contact.last_name
        )

        contact.email = request.POST.get(
            f"contact_email_{contact.id}",
            contact.email
        )

        contact.phone = request.POST.get(
            f"contact_phone_{contact.id}",
            contact.phone
        )

        contact.save()



    # =========================
    # NEW CONTACTS
    # =========================

    first_names = request.POST.getlist(
        "new_contact_first_name"
    )

    last_names = request.POST.getlist(
        "new_contact_last_name"
    )

    emails = request.POST.getlist(
        "new_contact_email"
    )

    phones = request.POST.getlist(
        "new_contact_phone"
    )


    for i in range(len(first_names)):

        if not (
            first_names[i].strip()
            or last_names[i].strip()
        ):
            continue


        CustomerContact.objects.create(
            customer=customer,
            first_name=first_names[i],
            last_name=last_names[i],
            email=emails[i],
            phone=phones[i],
        )



    # =========================
    # LOCATION DELETE
    # =========================

    delete_location_id = request.POST.get(
        "delete_location_id"
    )

    if delete_location_id:

        CustomerLocation.objects.filter(
            id=delete_location_id,
            customer=customer
        ).delete()

        return redirect(
            "invoices:customers_detail",
            customer.id
        )



    # =========================
    # LOCATION UPDATE
    # =========================

    for location in customer.locations.all():

        location.name = request.POST.get(
            f"location_name_{location.id}",
            location.name
        )

        location.street = request.POST.get(
            f"location_street_{location.id}",
            location.street
        )

        location.zip_code = request.POST.get(
            f"location_zip_{location.id}",
            location.zip_code
        )

        location.city = request.POST.get(
            f"location_city_{location.id}",
            location.city
        )

        location.country = request.POST.get(
            f"location_country_{location.id}",
            location.country
        )

        location.save()



    # =========================
    # NEW LOCATIONS
    # =========================

    names = request.POST.getlist(
        "new_location_name"
    )

    streets = request.POST.getlist(
        "new_location_street"
    )

    zips = request.POST.getlist(
        "new_location_zip"
    )

    cities = request.POST.getlist(
        "new_location_city"
    )

    countries = request.POST.getlist(
        "new_location_country"
    )


    for i in range(len(names)):

        if not names[i].strip():
            continue


        CustomerLocation.objects.create(
            customer=customer,
            name=names[i],
            street=streets[i],
            zip_code=zips[i],
            city=cities[i],
            country=countries[i],
        )


    return redirect(
        "invoices:customers_detail",
        customer.id
    )

@login_required
@permission_required("invoices_customers_archive")
def customers_archive(request, customer_id):
    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    if request.method == "POST":
        customer.active = False
        customer.save()

    return redirect(
        "invoices:customers_overview"
    )


@login_required
@permission_required("invoices_customers_activate")
def customers_reactivate(request, customer_id):
    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    if request.method == "POST":
        customer.active = True
        customer.save()

    return redirect(
        "invoices:customers_overview"
    )


@login_required
@permission_required("invoices_customers_detail_view")
def customers_detail(request, customer_id):

    customer = get_object_or_404(
        Customer.objects.prefetch_related(
            "contacts",
            "locations",
            "projects",
        ),
        id=customer_id
    )

    form = CustomerForm(
        instance=customer
    )

    return render(
        request,
        "invoices/customers/detail.html",
        {
            "customer": customer,
            "form": form,
        }
    )






































@login_required
@permission_required("invoices_items_view")
def items_overview(request):
    units = Unit.objects.all()
    items = Item.objects.select_related(
        "unit"
    ).all()

    table = ItemTable(items)
    table.types = Item.ItemType.choices
    table.units = Unit.objects.order_by("name")
    table.categories = Category.objects.order_by("name")
    table.suppliers = Supplier.objects.order_by("name")

    RequestConfig(
        request,
        paginate=False
    ).configure(table)

    return render(
        request,
        "invoices/items/overview.html",
        {
            "table": table,
        }
    )

@login_required
@permission_required("invoices_items_add")
def items_add(request):
    if request.method == "POST":
        form = ItemForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("invoices:items_overview")

    else:
        form = ItemForm()

    return render(request, "invoices/items/add.html", {
        "form": form
    })

@login_required
@permission_required("invoices_items_edit")
def items_edit(request, item_id):
    if request.method != "POST":
        print("Invalid request method for items_edit")
        return redirect(
            "invoices:items_overview"
        )



    item = get_object_or_404(
        Item,
        id=item_id
    )


    form = ItemForm(
        request.POST,
        instance=item
    )
    if not form.is_valid():
        print(form.errors.as_json())

    if form.is_valid():
        form.save()


    return redirect(
        "invoices:items_overview"
    )



@login_required
@permission_required("invoices_items_delete")
def items_delete(request,item_id):

    item = get_object_or_404(
        Item,
        id=item_id
    )

    if request.method == "POST":
        item.delete()

    return redirect(
        "invoices:items_overview"
    )




































@login_required
def ajax_contacts(request, customer_id):

    contacts = CustomerContact.objects.filter(customer_id=customer_id)

    data = [
        {"id": c.id, "text": str(c)}
        for c in contacts
    ]

    return JsonResponse(data, safe=False)


@login_required
def ajax_locations(request, customer_id):

    locations = CustomerLocation.objects.filter(customer_id=customer_id)

    data = [
        {"id": l.id, "text": str(l)}
        for l in locations
    ]

    return JsonResponse(data, safe=False)



@login_required
def ajax_invoicedata(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )


    if project.customer:

        contacts = [
            {
                "id": c.id,
                "text": str(c)
            }
            for c in project.customer.contacts.all()
        ]


        locations = [
            {
                "id": l.id,
                "text": str(l)
            }
            for l in project.customer.locations.all()
        ]


        return JsonResponse({
            "has_customer": True,
            "contacts": contacts,
            "locations": locations,
        })


    return JsonResponse({
        "has_customer": False
    })



@login_required
def ajax_invoiceitemsources(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id
    )


    data = {
        "has_project": False,
        "time_entries": [],
        "expenses": [],
    }


    if invoice.project:

        data["has_project"] = True


        data["time_entries"] = [
            {
                "id": t.id,
                "text": str(t)
            }
            for t in invoice.project.time_entries.all()
        ]


        data["expenses"] = [
            {
                "id": e.id,
                "text": str(e)
            }
            for e in invoice.project.expenses.all()
        ]


    return JsonResponse(data)



@login_required
def ajax_invoice_item_data(request):

    source = request.GET.get("source")
    source_id = request.GET.get("id")

    data = {}

    if source == "item":

        item = get_object_or_404(
            Item,
            id=source_id
        )

        data = {
            "description": item.description,
            "quantity": "1.00",
            "unit": item.unit.name,
            "unit_price_net": str(item.price_net),
            "unit_tax_rate": str(item.tax_rate),
        }


    elif source == "time":

        entry = get_object_or_404(
            TimeEntry,
            id=source_id,
        )

        data = {
            "description": (
                f"Arbeitszeit "
                f"{entry.start.strftime('%d.%m.%Y')} - "
                f"{entry.end.strftime('%d.%m.%Y')}"
            ),

            "quantity": str(
                entry.duration_hours
            ),

            "unit": "Stunden",

            "unit_price_net": str(
                entry.project.hourly_rate
            ),
        }


    elif source == "expense":

        expense = get_object_or_404(
            Expense,
            id=source_id
        )

        data = {
            "description": str(expense.name),
            "quantity": "1.00",
            "unit": "Stück",
            "unit_price_net": str(expense.amount),
        }


    return JsonResponse(data)








































@login_required
@permission_required("invoices_invoices_view")
def invoices_invoices_overview(request):
    status = request.GET.get("status")

    invoices = Invoice.objects.select_related("customer", "project").all()

    if status:
        invoices = invoices.filter(status=status)

    table = InvoiceTable(invoices)

    RequestConfig(
        request,
        paginate=False
    ).configure(table)

    return render(
        request,
        "invoices/invoices/overview.html",
        {
            "table": table
        }
    )




@login_required
@permission_required("invoices_invoices_customer_add")
def invoice_add_customer(request):

    form = CustomerInvoiceForm(request.POST or None)

    if form.is_valid():
        invoice = form.save(commit=False)

        customer = invoice.customer
        contact = form.cleaned_data.get("contact")
        location = form.cleaned_data.get("location")

        invoice.tax_number = customer.tax_number
        invoice.vat_number = customer.vat_number

        # SNAPSHOT CONTACT
        if contact:
            invoice.contact_name = f"{contact.first_name} {contact.last_name}"
            invoice.contact_email = contact.email
            invoice.contact_phone = contact.phone

        # SNAPSHOT LOCATION
        if location:
            invoice.location_name = location.name
            invoice.location_street = location.street
            invoice.location_city = location.city
            invoice.location_zip = location.zip_code
            invoice.location_country = location.country

        invoice.save()
        return redirect("invoices:invoices_invoices_overview")

    return render(request, "invoices/invoices/add_customer.html", {
        "form": form
    })


@login_required
@permission_required("invoices_invoices_project_add")
def invoice_add_project(request):
    form = ProjectInvoiceForm(request.POST or None)
    if form.is_valid():
        invoice = form.save(commit=False)

        project = form.cleaned_data.get("project")
        invoice.project = project

        if project and project.customer:
            customer = project.customer
            invoice.customer = customer
            invoice.tax_number = customer.tax_number
            invoice.vat_number = customer.vat_number
            contact = form.cleaned_data.get("contact")
            if contact:
                invoice.contact_name = (
                    f"{contact.first_name} {contact.last_name}"
                )
                invoice.contact_email = contact.email
                invoice.contact_phone = contact.phone
            location = form.cleaned_data.get("location")
            if location:
                invoice.location_name = location.name
                invoice.location_street = location.street
                invoice.location_zip = location.zip_code
                invoice.location_city = location.city
                invoice.location_country = location.country
        else:
            invoice.customer = None
            invoice.contact_name = form.cleaned_data.get(
                "contact_name_manual",
                ""
            )
            invoice.contact_email = form.cleaned_data.get(
                "contact_email_manual",
                ""
            )
            invoice.contact_phone = form.cleaned_data.get(
                "contact_phone_manual",
                ""
            )
            invoice.location_name = form.cleaned_data.get(
                "location_name_manual",
                ""
            )
            invoice.location_street = form.cleaned_data.get(
                "location_street_manual",
                ""
            )
            invoice.location_zip = form.cleaned_data.get(
                "location_zip_manual",
                ""
            )
            invoice.location_city = form.cleaned_data.get(
                "location_city_manual",
                ""
            )
            invoice.location_country = form.cleaned_data.get(
                "location_country_manual",
                ""
            )
        invoice.save()
        return redirect(
            "invoices:invoices_invoices_overview"
        )
    return render(
        request,
        "invoices/invoices/add_project.html",
        {
            "form": form
        }
    )









@login_required
@permission_required("invoices_invoices_invoices_view")
def invoices_detail(request, invoice_id):

    invoice = get_object_or_404(
        Invoice.objects.select_related(
            "customer",
            "project",
        ).prefetch_related(
            "items__item",
            "items__time_entry",
            "items__expense",
            "reminders",
        ),
        id=invoice_id
    )


    items = invoice.items.all()


    reminders = invoice.reminders.all()


    total_net = sum(
        (i.unit_price_net or Decimal("0.00")) *
        (i.quantity or Decimal("0.00"))
        for i in items
    )


    show_service_date = any(
        item.service_period_from
        for item in items
    )

    table = InvoiceItemTable(items)

    if not show_service_date:
        table.columns.hide("service_period")

    if invoice.status != "draft":
        table.columns.hide("actions")

    RequestConfig(
        request,
        paginate=False
    ).configure(table)

    return render(
        request,
        "invoices/invoices/detail.html",
        {
            "invoice": invoice,
            "table": table,
            "reminders": reminders,
            "total_net": total_net,
            "show_service_date": show_service_date,
        }
    )









@login_required
@permission_required("invoices_invoices_invoices_item_add")
def invoice_item_add(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id
    )

    if invoice.status != "draft":
        return redirect("invoices:invoices_detail",invoice.id)


    if request.method == "POST":

        form = InvoiceItemForm(
            request.POST,
            invoice=invoice
        )

        if form.is_valid():

            item = form.save(
                commit=False
            )

            item.invoice = invoice
            item.save()


            return redirect(
                "invoices:invoices_detail",
                invoice.id
            )


    else:

        form = InvoiceItemForm(
            invoice=invoice
        )


    return render(
        request,
        "invoices/invoices/item_add.html",
        {
            "form": form,
            "invoice": invoice
        }
    )



@login_required
@permission_required("invoices_invoices_invoices_preview")
def invoices_preview(request, invoice_id):

    invoice = get_object_or_404(
        Invoice.objects.select_related(
            "customer",
            "project",
        ),
        id=invoice_id
    )

    if invoice.status != "draft":
        return redirect("invoices:invoices_detail",invoice.id)
    
    items = invoice.items.all()

    # ==========================
    # Summen berechnen
    # ==========================
    total_net = Decimal("0.00")
    tax_summary = defaultdict(
        lambda: Decimal("0.00")
    )
    for item in items:
        item_net = Decimal(str(item.calculated_total_net))
        total_net += item_net
        tax_rate = Decimal(str(item.unit_tax_rate))
        tax_amount = (
            item_net *
            tax_rate /
            Decimal("100")
        )
        tax_summary[tax_rate] += tax_amount

    total_tax = sum(
        tax_summary.values(),
        Decimal("0.00")
    )

    total_gross = (
        total_net +
        total_tax
    )

    show_service_date = any(
        item.service_period_from
        for item in items
    )

    # ==========================
    # Firma
    # ==========================
    company = CompanySetting.objects.first()
    return render(
        request,
        "invoices/invoices/preview.html",
        {
            "invoice": invoice,
            "items": items,

            "company": company,


            # Summen
            "total_net": total_net,
            "tax_summary": dict(tax_summary),
            "total_tax": total_tax,
            "total_gross": total_gross,

            "show_service_date": show_service_date,
        }
    )






@login_required
@permission_required("invoices_invoices_invoices_download")
def invoices_download(request, invoice_id):

    invoice = get_object_or_404(
        Invoice.objects.select_related(
            "customer",
            "project",
        ),
        id=invoice_id
    )


    # ==========================
    # Bestehendes PDF zurückgeben
    # ==========================

    if invoice.status != "draft" and invoice.pdf_file:
        return FileResponse(
            invoice.pdf_file.open("rb"),
            as_attachment=True,
            filename=invoice.pdf_file.name.split("/")[-1],
        )


    items = invoice.items.all()


    # ==========================
    # Summen
    # ==========================

    total_net = Decimal("0.00")

    tax_summary = defaultdict(
        lambda: Decimal("0.00")
    )


    for item in items:

        item_net = Decimal(
            str(item.calculated_total_net)
        )

        total_net += item_net

        tax_rate = Decimal(
            str(item.unit_tax_rate)
        )

        tax_amount = (
            item_net *
            tax_rate /
            Decimal("100")
        )

        tax_summary[tax_rate] += tax_amount


    total_tax = sum(
        tax_summary.values(),
        Decimal("0.00")
    )

    total_gross = total_net + total_tax


    company = CompanySetting.objects.first()
    number_settings = company.number_settings
    invoice.invoice_number = generate_document_number(
        number_settings.invoice_format,
        number_settings.invoice_next_number,
    )
    number_settings.invoice_next_number += 1
    number_settings.save(update_fields=["invoice_next_number"])

    company = CompanySetting.objects.first()
    invoice.is_small_business = company.is_small_business

    invoice.save(update_fields=["invoice_number", "is_small_business"])

    # ==========================
    # PDF HTML
    # ==========================

    show_service_date = any(
        item.service_period_from
        for item in items
    )

    html_string = render_to_string(
        "invoices/invoices/pdf.html",
        {
            "invoice": invoice,
            "items": items,
            "company": company,
            "total_net": total_net,
            "tax_summary": dict(tax_summary),
            "total_tax": total_tax,
            "total_gross": total_gross,
            "show_service_date": show_service_date,
        }
    )


    # ==========================
    # PDF erstellen
    # ==========================

    pdf_file = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()


    filename = f"Rechnung-{invoice.invoice_number}.pdf"


    # ==========================
    # PDF speichern
    # ==========================

    invoice.pdf_file.save(
        filename,
        ContentFile(pdf_file),
        save=False
    )

    invoice.pdf_generated_at = timezone.now()
    invoice.status = "sent"

    invoice.save(
        update_fields=[
            "pdf_file",
            "pdf_generated_at",
            "status",
        ]
    )




    return FileResponse(
        io.BytesIO(pdf_file),
        as_attachment=True,
        filename=filename
    )





@login_required
@permission_required("invoices_invoices_invoices_item_delete")
def invoice_item_delete(request,invoice_id,item_id):
    invoice = get_object_or_404(
        Invoice.objects.select_related(
            "customer",
            "project",
        ),
        id=invoice_id
    )

    item = get_object_or_404(
        InvoiceItem,
        id=item_id,
        invoice_id=invoice_id
    )

    if invoice.status != "draft":
        return redirect("invoices:invoices_detail",invoice.id)

    if request.method == "POST":
        item.delete()

    return redirect(
        "invoices:invoices_detail",
        invoice_id=invoice_id
    )




@login_required
@permission_required("invoices_invoices_invoices_cancel")
def invoices_cancel(request, invoice_id):

    invoice = get_object_or_404(
        Invoice.objects.select_related(
            "customer",
            "project",
        ),
        id=invoice_id,
    )


    # ==========================
    # Existierendes Storno zurückgeben
    # ==========================

    if invoice.status == Invoice.Status.CANCELED and invoice.pdf_canceled_file:

        return FileResponse(
            invoice.pdf_canceled_file.open("rb"),
            as_attachment=True,
            filename=invoice.pdf_canceled_file.name.split("/")[-1],
        )


    # ==========================
    # Nur finale Rechnungen stornierbar
    # ==========================

    if invoice.status not in [
        Invoice.Status.SENT,
        Invoice.Status.PAID,
        Invoice.Status.OVERDUE,
    ]:
        return redirect(
            "invoices:invoices_detail",
            invoice.id,
        )


    company = CompanySetting.objects.first()
    number_settings = company.number_settings


    # ==========================
    # Stornonummer
    # ==========================

    invoice.cancel_number = generate_document_number(
        number_settings.cancel_format,
        number_settings.cancel_next_number,
    )


    number_settings.cancel_next_number += 1

    number_settings.save(
        update_fields=[
            "cancel_next_number"
        ]
    )


    # ==========================
    # Positionen
    # ==========================

    items = invoice.items.all()


    # ==========================
    # Bereits bezahlt
    # ==========================

    paid_amount = invoice.paid_amount


    # ==========================
    # Rückerstattung berechnen
    # ==========================

    refund_amount = min(
        paid_amount,
        invoice.total_amount
    )


    show_service_date = any(
        item.service_period_from
        for item in items
    )


    tax_summary = defaultdict(
        lambda: Decimal("0.00")
    )

    for item in items:

        item_net = item.calculated_total_net

        tax_amount = (
            item_net *
            item.unit_tax_rate /
            Decimal("100")
        )

        tax_summary[item.unit_tax_rate] += tax_amount

    # ==========================
    # PDF HTML
    # ==========================

    html_string = render_to_string(
        "invoices/invoices/pdf_cancel.html",
        {
            "invoice": invoice,
            "items": items,
            "company": company,
            "cancel_date": timezone.now(),
            "cancel_number": invoice.cancel_number,
            "paid_amount": paid_amount,
            "refund_amount": refund_amount,
            "total_net": invoice.total_net,
            "total_tax": invoice.total_tax,
            "total_gross": invoice.total_amount,
            "show_service_date": show_service_date,
            "tax_summary": dict(tax_summary),
        },
    )


    # ==========================
    # PDF erstellen
    # ==========================

    pdf_file = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()


    filename = (
        f"Stornorechnung-{invoice.cancel_number}.pdf"
    )


    invoice.pdf_canceled_file.save(
        filename,
        ContentFile(pdf_file),
        save=False,
    )


    invoice.pdf_canceled_generated_at = timezone.now()

    invoice.status = Invoice.Status.CANCELED


    invoice.save(
        update_fields=[
            "pdf_canceled_file",
            "pdf_canceled_generated_at",
            "status",
            "cancel_number",
        ]
    )


    return FileResponse(
        io.BytesIO(pdf_file),
        as_attachment=True,
        filename=filename,
    )



@login_required
@permission_required("invoices_invoices_invoices_delete")
def invoices_delete(request, invoice_id):
    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
    )

    if invoice.status != Invoice.Status.DRAFT:
        return redirect(
            "invoices:invoices_detail",
            invoice_id=invoice.id,
        )

    invoice.delete()
    return redirect("invoices:invoices_invoices_overview",)






















def create_invoice_income(invoice):
    from finance.models import Income

    if Income.objects.filter(
        invoice=invoice
    ).exists():
        return

    last_payment = invoice.payments.order_by(
        "-date"
    ).first()

    if not last_payment:
        return

    Income.objects.create(
        invoice=invoice,
        amount=invoice.paid_invoice_amount,
        date=last_payment.date,
        name=f"Zahlung Rechnung {invoice.invoice_number}",
        project=invoice.project,
        payment_method=last_payment.payment_method,
        created_by=last_payment.created_by,
    )

def allocate_invoice_payment(payment):
    remaining = payment.amount
    invoice = payment.invoice
    reminders = invoice.reminders.filter(
        status__in=[
            Reminder.Status.SENT,
            Reminder.Status.EXPIRED,
        ]
    ).order_by("level")

    for reminder in reminders:
        already_paid = reminder.payment_allocations.aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0.00")
        open_fee = reminder.fee - already_paid
        if open_fee <= 0:
            continue
        allocation_amount = min(
            remaining,
            open_fee
        )
        if allocation_amount > 0:
            InvoicePaymentAllocation.objects.create(
                payment=payment,
                reminder=reminder,
                amount=allocation_amount
            )
            remaining -= allocation_amount
        if remaining <= 0:
            break
    if remaining > 0:
        InvoicePaymentAllocation.objects.create(
            payment=payment,
            reminder=None,
            amount=remaining
        )

def update_invoice_payment_status(invoice):
    # Mahnungen prüfen
    reminders = invoice.reminders.filter(
        status__in=[
            Reminder.Status.SENT,
            Reminder.Status.EXPIRED,
        ]
    )
    for reminder in reminders:
        if reminder.paid_amount >= reminder.fee:
            reminder.status = Reminder.Status.PAID
            reminder.save(
                update_fields=[
                    "status"
                ]
            )
    if invoice.paid_invoice_amount >= invoice.total_amount:
        if invoice.status != Invoice.Status.PAID:
            invoice.status = Invoice.Status.PAID
            invoice.save(
                update_fields=[
                    "status"
                ]
            )

            if invoice.project:
                create_invoice_income(invoice)


@login_required
@permission_required("invoices_invoices_invoices_paid")
def invoices_paid(request, invoice_id):
    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
    )

    if invoice.status not in [
        Invoice.Status.SENT,
        Invoice.Status.OVERDUE,
    ]:
        return redirect(
            "invoices:invoices_detail",
            invoice_id=invoice.id,
        )

    if request.method == "POST":
        form = InvoicePaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.created_by = request.user
            payment.save()
            allocate_invoice_payment(payment)
            update_invoice_payment_status(invoice)
            return redirect(
                "invoices:invoices_detail",
                invoice_id=invoice.id,
            )
        else:
            print(form.errors)
    else:
        form = InvoicePaymentForm()
    return render(
        request,
        "invoices/invoices/add_payment.html",
        {
            "form": form,
            "invoice": invoice,
        }
    )


















































































@login_required
@permission_required("invoices_offers_view")
def invoices_offers_overview(request):
    status = request.GET.get("status")

    offers = Offer.objects.select_related("customer",).all()

    if status:
        offers = offers.filter(status=status)
    table = OfferTable(offers)

    RequestConfig(
        request,
        paginate=False
    ).configure(table)
    return render(
        request,
        "invoices/offers/overview.html",
        {
            "table": table
        }
    )




@login_required
@permission_required("invoices_offers_add")
def invoices_offers_add(request):

    form = OfferForm(request.POST or None)

    if form.is_valid():
        offer = form.save(commit=False)

        customer = offer.customer
        contact = form.cleaned_data.get("contact")
        location = form.cleaned_data.get("location")

        offer.tax_number = customer.tax_number
        offer.vat_number = customer.vat_number

        # SNAPSHOT CONTACT
        if contact:
            offer.contact_name = f"{contact.first_name} {contact.last_name}"
            offer.contact_email = contact.email
            offer.contact_phone = contact.phone

        # SNAPSHOT LOCATION
        if location:
            offer.location_name = location.name
            offer.location_street = location.street
            offer.location_city = location.city
            offer.location_zip = location.zip_code
            offer.location_country = location.country

        offer.save()
        return redirect("invoices:invoices_offers_overview")

    return render(request, "invoices/offers/add.html", {
        "form": form
    })






@login_required
@permission_required("invoices_offers_offers_delete")
def offers_delete(request, offer_id):
    offer = get_object_or_404(
        Offer,
        id=offer_id,
    )

    if offer.status != Offer.Status.DRAFT:
        return redirect(
            "invoices:offers_detail",
            offer_id=offer.id,
        )

    offer.delete()
    return redirect("invoices:invoices_offers_overview",)






@login_required
@permission_required("invoices_offers_offers_view")
def offers_detail(request, offer_id):
    offer = get_object_or_404(
        Offer.objects.select_related(
            "customer",
        ),
        id=offer_id
    )


    items = offer.items.select_related(
        "item",
    )


    total_net = sum(
        (i.unit_price_net or Decimal("0.00")) *
        (i.quantity or Decimal("0.00"))
        for i in items
    )

    table = OfferItemTable(items)

    table.offer = offer

    if offer.status != "draft":
        table.columns.hide("actions")

    RequestConfig(
        request,
        paginate=False
    ).configure(table)

    return render(
        request,
        "invoices/offers/detail.html",
        {
            "offer": offer,
            "table": table,
            "total_net": total_net
        }
    )









@login_required
@permission_required("invoices_offers_offers_item_add")
def offers_item_add(request, offer_id):

    offer = get_object_or_404(
        Offer,
        id=offer_id
    )

    if offer.status != "draft":
        return redirect("invoices:offers_detail",offer.id)


    if request.method == "POST":

        form = OfferItemForm(
            request.POST,
            offer=offer
        )

        if form.is_valid():

            item = form.save(
                commit=False
            )

            item.offer = offer
            item.save()


            return redirect(
                "invoices:offers_detail",
                offer.id
            )


    else:

        form = OfferItemForm(
            offer=offer
        )


    return render(
        request,
        "invoices/offers/item_add.html",
        {
            "form": form,
            "offer": offer
        }
    )






@login_required
@permission_required("invoices_offers_offers_item_delete")
def offers_item_delete(request,offer_id,item_id):
    offer = get_object_or_404(
        Offer.objects.select_related(
            "customer",
        ),
        id=offer_id
    )

    item = get_object_or_404(
        OfferItem,
        id=item_id,
        offer_id=offer_id
    )

    if offer.status != "draft":
        return redirect("invoices:offers_detail",offer.id)

    if request.method == "POST":
        item.delete()

    return redirect(
        "invoices:offers_detail",
        offer_id=offer_id
    )









@login_required
@permission_required("invoices_offers_offers_preview")
def offers_preview(request, offer_id):

    offer = get_object_or_404(
        Offer.objects.select_related(
            "customer",
        ),
        id=offer_id
    )

    if offer.status != "draft":
        return redirect("invoices:offers_detail",offer.id)
    
    items = offer.items.all()

    # ==========================
    # Summen berechnen
    # ==========================
    total_net = Decimal("0.00")
    tax_summary = defaultdict(
        lambda: Decimal("0.00")
    )
    for item in items:
        item_net = Decimal(str(item.calculated_total_net))
        total_net += item_net
        tax_rate = Decimal(str(item.unit_tax_rate))
        tax_amount = (
            item_net *
            tax_rate /
            Decimal("100")
        )
        tax_summary[tax_rate] += tax_amount

    total_tax = sum(
        tax_summary.values(),
        Decimal("0.00")
    )

    total_gross = (
        total_net +
        total_tax
    )

    # ==========================
    # Firma
    # ==========================
    company = CompanySetting.objects.first()
    return render(
        request,
        "invoices/offers/preview.html",
        {
            "offer": offer,
            "items": items,

            "company": company,


            # Summen
            "total_net": total_net,
            "tax_summary": dict(tax_summary),
            "total_tax": total_tax,
            "total_gross": total_gross,
        }
    )






@login_required
@permission_required("invoices_offers_offers_download")
def offers_download(request, offer_id):

    offer = get_object_or_404(
        Offer.objects.select_related(
            "customer",
        ),
        id=offer_id
    )


    # ==========================
    # Bestehendes PDF zurückgeben
    # ==========================

    if offer.status != "draft" and offer.pdf_file:

        return FileResponse(
            offer.pdf_file.open("rb"),
            as_attachment=True,
            filename=offer.pdf_file.name.split("/")[-1],
        )


    items = offer.items.all()


    # ==========================
    # Summen
    # ==========================

    total_net = Decimal("0.00")

    tax_summary = defaultdict(
        lambda: Decimal("0.00")
    )


    for item in items:

        item_net = Decimal(
            str(item.calculated_total_net)
        )

        total_net += item_net

        tax_rate = Decimal(
            str(item.unit_tax_rate)
        )

        tax_amount = (
            item_net *
            tax_rate /
            Decimal("100")
        )

        tax_summary[tax_rate] += tax_amount


    total_tax = sum(
        tax_summary.values(),
        Decimal("0.00")
    )

    total_gross = total_net + total_tax

    company = CompanySetting.objects.first()
    number_settings = company.number_settings
    offer.offer_number = generate_document_number(
        number_settings.offer_format,
        number_settings.offer_next_number,
    )
    number_settings.offer_next_number += 1
    number_settings.save(update_fields=["offer_next_number"])
    offer.save(update_fields=["offer_number"])

    # ==========================
    # PDF HTML
    # ==========================

    html_string = render_to_string(
        "invoices/offers/pdf.html",
        {
            "offer": offer,
            "items": items,
            "company": company,
            "total_net": total_net,
            "tax_summary": dict(tax_summary),
            "total_tax": total_tax,
            "total_gross": total_gross,
        }
    )


    # ==========================
    # PDF erstellen
    # ==========================

    pdf_file = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()


    filename = f"Angebot-{offer.offer_number}.pdf"


    # ==========================
    # PDF speichern
    # ==========================

    offer.pdf_file.save(
        filename,
        ContentFile(pdf_file),
        save=False
    )

    offer.pdf_generated_at = timezone.now()
    offer.status = "sent"

    offer.save(
        update_fields=[
            "pdf_file",
            "pdf_generated_at",
            "status",
        ]
    )


    return FileResponse(
        io.BytesIO(pdf_file),
        as_attachment=True,
        filename=filename
    )








@login_required
@permission_required("invoices_offers_offers_status")
def offers_accept(request, offer_id):

    offer = get_object_or_404(
        Offer,
        id=offer_id,
    )

    if offer.status != "sent":
        return redirect(
            "invoices:offers_detail",
            offer_id=offer.id,
        )

    offer.status = "accepted"

    offer.save(
        update_fields=[
            "status",
        ]
    )

    return redirect(
        "invoices:offers_detail",
        offer_id=offer.id,
    )

@login_required
@permission_required("invoices_offers_offers_status")
def offers_reject(request, offer_id):

    offer = get_object_or_404(
        Offer,
        id=offer_id,
    )

    if offer.status != "sent":
        return redirect(
            "invoices:offers_detail",
            offer_id=offer.id,
        )

    offer.status = "rejected"

    offer.save(
        update_fields=[
            "status",
        ]
    )

    return redirect(
        "invoices:offers_detail",
        offer_id=offer.id,
    )












































































@login_required
@permission_required("invoices_reminders_view")
def invoices_reminders_overview(request):
    status = request.GET.get("status")
    reminders = Reminder.objects.select_related("invoice").all()
    if status:
        reminders = reminders.filter(status=status)
    table = ReminderTable(reminders)

    RequestConfig(
        request,
        paginate=False
    ).configure(table)

    return render(
        request,
        "invoices/reminders/overview.html",
        {
            "table": table,
        }
    )


@login_required
@permission_required("invoices_reminders_add")
def invoices_reminders_add(request):
    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            invoice = reminder.invoice
            reminders = invoice.reminders.exclude(
                status=Reminder.Status.CANCELED
            ).order_by("-level")


            # ==========================
            # Vorhandene Mahnung prüfen
            # ==========================
            if reminders.exists():
                last_reminder = reminders.first()
                if last_reminder.status not in [
                    Reminder.Status.EXPIRED,
                ]:
                    return redirect("invoices:invoices_reminders_overview",)
                next_level = last_reminder.level + 1
            else:
                next_level = 1

            if next_level > 3:
                return redirect(
                    "invoices:invoices_reminders_overview",)


            reminder.level = next_level
            reminder.status = Reminder.Status.DRAFT

            reminder.save()


            return redirect(
                "invoices:reminders_detail",
                reminder_id=reminder.pk,
            )

    else:
        form = ReminderForm()


    return render(
        request,
        "invoices/reminders/add.html",
        {
            "form": form,
        },
    )




@login_required
@permission_required("invoices_reminders_reminders_view")
def reminders_detail(request, reminder_id):
    reminder = get_object_or_404(
        Reminder.objects.select_related("invoice",),
        id=reminder_id
    )

    return render(
        request,
        "invoices/reminders/detail.html",
        {
            "reminder": reminder
        }
    )

@login_required
@permission_required("invoices_reminders_reminders_cancel")
def reminders_cancel(request, reminder_id):

    reminder = get_object_or_404(
        Reminder,
        id=reminder_id,
    )

    if reminder.status != "sent" and reminder.status != "draft":
        return redirect(
            "invoices:reminders_detail",
            reminder_id=reminder.id,
        )

    reminder.status = "canceled"

    reminder.save(
        update_fields=[
            "status",
        ]
    )

    return redirect(
        "invoices:reminders_detail",
        reminder_id=reminder.id,
    )


@login_required
@permission_required("invoices_reminders_reminders_delete")
def reminders_delete(request, reminder_id):
    reminder = get_object_or_404(
        Reminder,
        id=reminder_id,
    )

    if reminder.status != Reminder.Status.DRAFT:
        return redirect(
            "invoices:reminders_detail",
            reminder_id=reminder.id,
        )

    reminder.delete()
    return redirect("invoices:invoices_reminders_overview",)


@login_required
@permission_required("invoices_reminders_reminders_download")
def reminders_download(request, reminder_id):

    reminder = get_object_or_404(
        Reminder.objects.select_related(
            "invoice",
            "invoice__customer",
            "invoice__project",
        ),
        id=reminder_id
    )


    # ==========================
    # Bestehendes PDF zurückgeben
    # ==========================

    if reminder.pdf_file:
        return FileResponse(
            reminder.pdf_file.open("rb"),
            as_attachment=True,
            filename=reminder.pdf_file.name.split("/")[-1],
        )


    invoice = reminder.invoice

    payments = invoice.payments.order_by("date", "created_at")

    total_paid = sum(
        payment.amount
        for payment in payments
    )

    # ==========================
    # Rechnungsbetrag berechnen
    # ==========================

    items = invoice.items.all()

    total_net = Decimal("0.00")
    total_tax = Decimal("0.00")


    for item in items:

        item_net = Decimal(
            str(item.calculated_total_net)
        )

        total_net += item_net

        tax_rate = Decimal(
            str(item.unit_tax_rate)
        )

        total_tax += (
            item_net *
            tax_rate /
            Decimal("100")
        )


    invoice_amount = total_net + total_tax

    # ==========================
    # Vorherige Mahnungen
    # ==========================
    previous_reminders = (
        invoice.reminders
        .exclude(id=reminder.id)
        .exclude(status=Reminder.Status.CANCELED)
        .order_by("level")
    )

    total_previous_fees = sum(
        r.fee for r in previous_reminders
    )

    total_due = (
        invoice_amount
        + total_previous_fees
        + reminder.fee
    )

    open_amount = total_due - total_paid
    total_fees = (total_previous_fees + reminder.fee)

    company = CompanySetting.objects.first()


    # ==========================
    # Mahnungsnummer vergeben
    # ==========================

    if not reminder.reminder_number:

        number_settings = company.number_settings

        reminder.reminder_number = generate_document_number(
            number_settings.reminder_format,
            number_settings.reminder_next_number,
        )

        number_settings.reminder_next_number += 1

        number_settings.save(
            update_fields=[
                "reminder_next_number"
            ]
        )


    reminder.save(
        update_fields=[
            "reminder_number",
        ]
    )


    # ==========================
    # PDF HTML
    # ==========================

    html_string = render_to_string(
        "invoices/reminders/pdf.html",
        {
            "reminder": reminder,
            "invoice": invoice,
            "company": company,
            "invoice_amount": invoice_amount,
            "previous_reminders": previous_reminders,
            "total_previous_fees": total_previous_fees,
            "total_fees": total_fees,
            "payments": payments,
            "total_paid": total_paid,
            "total_due": total_due,
            "open_amount": open_amount,
        }
    )
    # ==========================
    # PDF erstellen
    # ==========================

    pdf_file = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()


    filename = f"Mahnung-{reminder.reminder_number}.pdf"


    reminder.pdf_file.save(
        filename,
        ContentFile(pdf_file),
        save=False
    )


    reminder.pdf_generated_at = timezone.now()
    reminder.status = Reminder.Status.SENT


    reminder.save(
        update_fields=[
            "pdf_file",
            "pdf_generated_at",
            "status",
        ]
    )


    return FileResponse(
        io.BytesIO(pdf_file),
        as_attachment=True,
        filename=filename
    )













@login_required
@permission_required("invoices_payments_view")
def invoices_payments_overview(request):

    payments = InvoicePayment.objects.select_related(
        "invoice",
        "invoice__customer",
        "payment_method",
        "created_by",
    ).order_by(
        "-date"
    )


    table = InvoicePaymentTable(
        payments
    )


    RequestConfig(
        request,
        paginate={
            "per_page": 25
        }
    ).configure(
        table
    )


    return render(
        request,
        "invoices/payments/overview.html",
        {
            "table": table,
        }
    )