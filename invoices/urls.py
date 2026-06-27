from django.urls import path
from . import views

app_name = "invoices"

urlpatterns = [
    path("", views.invoices_overview, name="overview"),


    # Kunden
    path("customers/", views.customers_overview, name="customers_overview"),
    path("customers/add/", views.customers_add, name="customers_add"),
    path("customers/<int:customer_id>/", views.customers_detail, name="customers_detail"),
    path("customers/<int:customer_id>/edit/", views.customers_edit, name="customers_edit"),
    path("customers/<int:customer_id>/archive/", views.customers_archive, name="customers_archive"),
    path("customers/<int:customer_id>/reactivate/", views.customers_reactivate, name="customers_reactivate"),


    # Items
    path("items/", views.items_overview, name="items_overview"),
    path("items/add/", views.items_add, name="items_add"),
    path("items/<int:item_id>/edit/", views.items_edit, name="items_edit"),
    path("items/<int:item_id>/delete/", views.items_delete, name="items_delete"),


    # Rechnungen
    path("invoices/", views.invoices_invoices_overview, name="invoices_invoices_overview"),
    path("invoices/<int:invoice_id>/", views.invoices_detail, name="invoices_detail"),

    path("invoices/add/customer/", views.invoice_add_customer, name="invoice_add_customer"),
    path("invoices/add/project/", views.invoice_add_project, name="invoice_add_project"),

    path("invoices/<int:invoice_id>/items/add/", views.invoice_item_add, name="invoice_item_add"),
    path("invoices/<int:invoice_id>/items/<int:item_id>/delete/", views.invoice_item_delete, name="invoice_item_delete"),

    path("invoices/<int:invoice_id>/preview/", views.invoices_preview, name="invoices_preview"),
    path("invoices/<int:invoice_id>/download/", views.invoices_download, name="invoices_download"),
    path("invoices/<int:invoice_id>/cancel/", views.invoices_cancel, name="invoices_cancel"),
    path("invoices/<int:invoice_id>/paid/", views.invoices_paid, name="invoices_paid"),
    path("invoices/<int:invoice_id>/overdue/", views.invoices_overdue, name="invoices_overdue"),
    path("invoices/<int:invoice_id>/delete/", views.invoices_delete, name="invoices_delete"),


    # Angebote
    path("offers/", views.invoices_offers_overview, name="invoices_offers_overview"),
    path("offers/<int:offer_id>/", views.offers_detail, name="offers_detail"),
    
    path("offers/add/", views.invoices_offers_add, name="invoices_offers_add"),

    path("offers/<int:offer_id>/items/add/", views.offers_item_add, name="offers_item_add"),
    path("offers/<int:offer_id>/items/<int:item_id>/delete/", views.offers_item_delete, name="offers_item_delete"),

    path("offers/<int:offer_id>/preview/", views.offers_preview, name="offers_preview"),
    path("offers/<int:offer_id>/download/", views.offers_download, name="offers_download"),
    path("offers/<int:offer_id>/accept/", views.offers_accept, name="offers_accept"),
    path("offers/<int:offer_id>/reject/", views.offers_reject, name="offers_reject"),
    path("offers/<int:offer_id>/expire/", views.offers_expire, name="offers_expire"),
    path("offers/<int:offer_id>/delete/", views.offers_delete, name="offers_delete"),

    # Mahnungen
    path("reminders/", views.invoices_reminders_overview, name="invoices_reminders_overview"),
    path("reminders/<int:reminder_id>/", views.reminders_detail, name="reminders_detail"),
    path("reminders/add/", views.invoices_reminders_add, name="invoices_reminders_add"),
    path("reminders/<int:reminder_id>/download/", views.reminders_download, name="reminders_download"),
    path("reminders/<int:reminder_id>/cancel/", views.reminders_cancel, name="reminders_cancel"),
    path("reminders/<int:reminder_id>/delete/", views.reminders_delete, name="reminders_delete"),
    path("reminders/<int:reminder_id>/expire/", views.reminders_expire, name="reminders_expire"),
    path("reminders/<int:reminder_id>/paid/", views.reminders_paid, name="reminders_paid"),


    # AJAX
    path("ajax/customer/<int:customer_id>/contacts/", views.ajax_contacts, name="ajax_contacts"),
    path("ajax/customer/<int:customer_id>/locations/", views.ajax_locations, name="ajax_locations"),
    path("ajax/project/<int:project_id>/invoice-data/", views.ajax_invoicedata, name="ajax_invoicedata"),
    path("ajax/invoice/<int:invoice_id>/sources/", views.ajax_invoiceitemsources, name="ajax_invoice_item_sources"),
    path("ajax/invoice-item-data/", views.ajax_invoice_item_data, name="ajax_invoice_item_data"),
]