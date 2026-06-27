import django_tables2 as tables
from .models import Item, Customer, Reminder, Invoice, InvoiceItem, Offer, OfferItem

class OfferItemTable(tables.Table):

    unit_price_net = tables.TemplateColumn(
        template_name="invoices/tables/offer_items/unit_price.html",
        verbose_name="Einzelpreis",
        orderable=False,
    )

    unit_tax_rate = tables.TemplateColumn(
        template_name="invoices/tables/offer_items/tax_rate.html",
        verbose_name="Steuerart",
        orderable=False,
    )

    total = tables.TemplateColumn(
        template_name="invoices/tables/offer_items/total.html",
        verbose_name="Gesamt",
        orderable=False,
    )

    actions = tables.TemplateColumn(
        template_name="invoices/tables/offer_items/actions.html",
        verbose_name="Aktionen",
        orderable=False,
    )

    class Meta:
        model = OfferItem

        fields = (
            "description",
            "quantity",
            "unit",
            "unit_price_net",
            "unit_tax_rate",
            "total",
            "actions",
        )

        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }


class OfferTable(tables.Table):

    customer = tables.Column(
        accessor="customer.company_name",
        verbose_name="Kunde"
    )

    status = tables.Column(
        accessor="get_status_display",
        verbose_name="Status"
    )

    issue_date = tables.DateColumn(
        format="d.m.Y",
        verbose_name="Datum"
    )

    due_date = tables.DateColumn(
        format="d.m.Y",
        verbose_name="Gültig bis"
    )

    actions = tables.TemplateColumn(
        template_name="invoices/tables/offers/actions.html",
        verbose_name="Aktion",
        orderable=False
    )

    class Meta:
        model = Offer

        fields = (
            "offer_number",
            "customer",
            "status",
            "issue_date",
            "due_date",
            "actions",
        )

        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }


class InvoiceItemTable(tables.Table):

    service_period = tables.TemplateColumn(
        template_name="invoices/tables/invoice_items/service_period.html",
        verbose_name="Leistungsdatum",
        orderable=False,
    )

    unit_price_net = tables.TemplateColumn(
        template_name="invoices/tables/invoice_items/unit_price.html",
        verbose_name="Einzelpreis",
        orderable=False,
    )

    unit_tax_rate = tables.TemplateColumn(
        template_name="invoices/tables/invoice_items/tax_rate.html",
        verbose_name="Steuerart",
        orderable=False,
    )

    total = tables.TemplateColumn(
        template_name="invoices/tables/invoice_items/total.html",
        verbose_name="Gesamt",
        orderable=False,
    )

    actions = tables.TemplateColumn(
        template_name="invoices/tables/invoice_items/actions.html",
        verbose_name="Aktionen",
        orderable=False,
    )

    class Meta:
        model = InvoiceItem

        fields = (
            "description",
            "service_period",
            "quantity",
            "unit",
            "unit_price_net",
            "unit_tax_rate",
            "total",
            "actions",
        )

        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }


class InvoiceTable(tables.Table):

    customer = tables.Column(
        accessor="customer.company_name",
        verbose_name="Kunde"
    )

    project = tables.Column(
        verbose_name="Projekt",
    )

    status = tables.Column(
        accessor="get_status_display",
        verbose_name="Status"
    )

    issue_date = tables.DateColumn(
        format="d.m.Y",
        verbose_name="Datum"
    )

    due_date = tables.DateColumn(
        format="d.m.Y",
        verbose_name="Fälligkeitsdatum"
    )


    actions = tables.TemplateColumn(
        template_name="invoices/tables/invoices/actions.html",
        verbose_name="Aktion",
        orderable=False
    )


    class Meta:

        model = Invoice

        fields = (
            "invoice_number",
            "customer",
            "project",
            "status",
            "issue_date",
            "due_date",
            "actions",
        )

        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }

class ReminderTable(tables.Table):

    invoice = tables.TemplateColumn(
        template_name="invoices/tables/reminders/invoice.html",
        verbose_name="Rechnung",
        orderable=False
    )

    level = tables.Column(
        verbose_name="Mahnstufe"
    )

    status = tables.Column(
        accessor="get_status_display",
        verbose_name="Status"
    )

    issue_date = tables.DateColumn(
        format="d.m.Y",
        verbose_name="Datum"
    )

    due_date = tables.DateColumn(
        format="d.m.Y",
        verbose_name="Neue Zahlungsfrist"
    )

    actions = tables.TemplateColumn(
        template_name="invoices/tables/reminders/actions.html",
        verbose_name="Aktion",
        orderable=False
    )


    class Meta:

        model = Reminder

        fields = (
            "reminder_number",
            "invoice",
            "level",
            "status",
            "issue_date",
            "due_date",
            "actions",
        )

        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }

class ItemTable(tables.Table):
    item_type = tables.TemplateColumn(
        template_name="invoices/tables/items/item_type.html",
        verbose_name="Typ",
        orderable=False
    )

    description = tables.TemplateColumn(
        template_name="invoices/tables/items/description.html",
        verbose_name="Beschreibung",
        orderable=False
    )

    unit = tables.TemplateColumn(
        template_name="invoices/tables/items/unit.html",
        verbose_name="Einheit",
        orderable=False
    )

    price_net = tables.TemplateColumn(
        template_name="invoices/tables/items/price_net.html",
        verbose_name="Preis Netto",
        orderable=False
    )

    tax_rate = tables.TemplateColumn(
        template_name="invoices/tables/items/tax_rate.html",
        verbose_name="MwSt. Satz (%)",
        orderable=False
    )

    actions = tables.TemplateColumn(
        template_name="invoices/tables/items/actions.html",
        verbose_name="Aktion",
        orderable=False
    )


    class Meta:
        model = Item
        fields = (
            "item_type",
            "description",
            "unit",
            "price_net",
            "tax_rate",
            "actions",
        )
        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }





class CustomerTable(tables.Table):
    toggle_prefix = "customer"

    detail_template = (
        "invoices/tables/customer/detail.html"
    )

    customer_number = tables.Column(
        verbose_name="Kunden-ID"
    )

    company_name = tables.Column(
        verbose_name="Name"
    )

    customer_type = tables.Column(
        accessor="get_customer_type_display",
        verbose_name="Typ"
    )

    phone = tables.Column(
        verbose_name="Telefon"
    )

    email = tables.Column(
        verbose_name="E-Mail"
    )

    tax_number = tables.Column(
        verbose_name="Steuernummer"
    )

    vat_number = tables.Column(
        verbose_name="UST-IdNr"
    )


    class Meta:
        model = Customer

        template_name = (
            "django_tables2/table_toggle.html"
        )

        fields = (
            "customer_number",
            "company_name",
            "customer_type",
            "phone",
            "email",
            "tax_number",
            "vat_number",
        )

        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }









class CustomerArchivedTable(tables.Table):
    toggle_prefix = "customer"

    detail_template = (
        "invoices/tables/customer/detail_archived.html"
    )

    customer_number = tables.Column(
        verbose_name="Kunden-ID"
    )

    company_name = tables.Column(
        verbose_name="Name"
    )

    customer_type = tables.Column(
        accessor="get_customer_type_display",
        verbose_name="Typ"
    )

    phone = tables.Column(
        verbose_name="Telefon"
    )

    email = tables.Column(
        verbose_name="E-Mail"
    )

    tax_number = tables.Column(
        verbose_name="Steuernummer"
    )

    vat_number = tables.Column(
        verbose_name="UST-IdNr"
    )


    class Meta:
        model = Customer

        template_name = (
            "django_tables2/table_toggle.html"
        )

        fields = (
            "customer_number",
            "company_name",
            "customer_type",
            "phone",
            "email",
            "tax_number",
            "vat_number",
        )

        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }