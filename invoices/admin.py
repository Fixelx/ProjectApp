from django.contrib import admin
from .models import (
    Customer,
    CustomerContact,
    CustomerLocation,
    Item,
    Invoice, 
    InvoiceItem,
    Unit,
    Reminder
)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "short_name",
    )

    search_fields = (
        "name",
        "short_name",
    )

class CustomerContactInline(admin.TabularInline):
    model = CustomerContact
    extra = 0


class CustomerLocationInline(admin.TabularInline):
    model = CustomerLocation
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "customer_number",
        "company_name",
        "customer_type",
        "phone",
        "email",
    )

    search_fields = (
        "customer_number",
        "company_name",
        "email",
        "phone",
        "tax_number",
        "vat_number",
    )

    list_filter = (
        "customer_type",
    )

    inlines = (
        CustomerContactInline,
        CustomerLocationInline,
    )


@admin.register(CustomerContact)
class CustomerContactAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "customer",
        "phone",
        "email",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "customer__company_name",
    )


@admin.register(CustomerLocation)
class CustomerLocationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "customer",
        "city",
        "country",
    )

    search_fields = (
        "name",
        "city",
        "street",
        "customer__company_name",
    )


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "item_type",
        "unit",
        "price_net",
    )

    search_fields = (
        "description",
    )

    list_filter = (
        "item_type",
        "unit",
    )






class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
        "customer",
        "project",
        "status",
        "issue_date",
        "due_date",
    )

    list_filter = (
        "status",
        "issue_date",
        "customer",
    )

    search_fields = (
        "invoice_number",
        "customer__company_name",
    )

    autocomplete_fields = (
        "customer",
        "project",
    )


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):

    list_display = (
        "description",
        "invoice",
        "quantity",
        "unit_price_net",
    )

    search_fields = (
        "description",
        "invoice__invoice_number",
    )

    autocomplete_fields = (
        "invoice",
        "item",
        "time_entry",
        "expense",
    )











from .models import (
    Offer,
    OfferItem,
)


class OfferItemInline(admin.TabularInline):
    model = OfferItem
    extra = 0


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):

    list_display = (
        "offer_number",
        "customer",
        "status",
        "issue_date",
        "due_date",
        "created_at",
    )

    list_filter = (
        "status",
        "issue_date",
    )

    search_fields = (
        "offer_number",
        "contact_name",
        "customer__company_name",
    )

    readonly_fields = (
        "created_at",
        "pdf_generated_at",
    )

    inlines = [
        OfferItemInline,
    ]


@admin.register(OfferItem)
class OfferItemAdmin(admin.ModelAdmin):

    list_display = (
        "offer",
        "description",
        "quantity",
        "unit",
        "unit_price_net",
        "unit_tax_rate",
        "created_at",
    )

    search_fields = (
        "description",
        "offer__offer_number",
    )

    autocomplete_fields = (
        "offer",
        "item",
    )


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_filter = (
        "level",
        "issue_date",
        "due_date",
        "pdf_generated_at",
    )

    search_fields = (
        "reminder_number",
    )

    readonly_fields = (
        "created_at",
        "pdf_generated_at",
    )

    ordering = ("-created_at",)
