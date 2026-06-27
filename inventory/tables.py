import django_tables2 as tables
from .models import ProjectInventoryItem, ShoppingItem, InventoryItem
import django_tables2 as tables

class InventoryGlobalTable(tables.Table):
    toggle_prefix = "inv"
    detail_template = "inventory/tables/inventory_global/edit_form.html"

    name = tables.Column(
        verbose_name="Name"
    )

    category = tables.Column(
        verbose_name="Kategorie"
    )

    available = tables.TemplateColumn(
        template_name="inventory/tables/inventory_global/available.html",
        verbose_name="Anzahl",
        orderable=False
    )

    location = tables.Column(
        verbose_name="Standort"
    )

    article_number = tables.Column(
        verbose_name="Artikelnummer"
    )

    class Meta:
        model = InventoryItem
        template_name = "django_tables2/table_toggle.html"
        fields = (
            "expand",
            "name",
            "category",
            "available",
            "location",
            "article_number",
        )
        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }


class InventoryAddTable(tables.Table):
    name = tables.Column(
        accessor="name",
        verbose_name="Name"
    )

    category = tables.Column(
        accessor="category",
        verbose_name="Kategorie"
    )

    available = tables.Column(
        accessor="available_quantity",
        verbose_name="Verfügbar"
    )

    article_number = tables.Column(
        accessor="article_number",
        verbose_name="Artikelnummer"
    )

    quantity = tables.TemplateColumn(
        template_name="inventory/tables/inventory_add/quantity.html",
        verbose_name="Anzahl hinzufügen",
        orderable=False
    )

    class Meta:
        model = InventoryItem
        fields = (
            "name",
            "category",
            "available",
            "article_number",
            "quantity",
        )
        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }

class ShoppingItemTable(tables.Table):

    name = tables.TemplateColumn(
        template_name="inventory/tables/shopping/name.html",
        verbose_name="Name"
    )

    category = tables.TemplateColumn(
        template_name="inventory/tables/shopping/category.html",
        verbose_name="Kategorie"
    )

    quantity = tables.TemplateColumn(
        template_name="inventory/tables/shopping/quantity.html",
        verbose_name="Anzahl"
    )

    supplier = tables.TemplateColumn(
        template_name="inventory/tables/shopping/supplier.html",
        verbose_name="Lieferant"
    )

    price = tables.TemplateColumn(
        template_name="inventory/tables/shopping/price.html",
        verbose_name="Preis"
    )

    description = tables.TemplateColumn(
        template_name="inventory/tables/shopping/description.html",
        verbose_name="Beschreibung"
    )

    actions = tables.TemplateColumn(
        template_name="inventory/tables/shopping/actions.html",
        verbose_name="Aktionen",
        orderable=False
    )

    class Meta:
        model = ShoppingItem
        fields = (
            "name",
            "category",
            "quantity",
            "supplier",
            "price",
            "description",
            "actions",
        )
        attrs = {
            "class": "w-full text-sm"
        }

class ProjectInventoryItemTable(tables.Table):

    name = tables.Column(
        accessor="item.name",
        verbose_name="Name"
    )

    category = tables.Column(
        accessor="item.category",
        verbose_name="Kategorie"
    )

    quantity = tables.TemplateColumn(
        template_name="inventory/tables/quantity.html",
        verbose_name="Anzahl"
    )

    location = tables.Column(
        accessor="item.location",
        verbose_name="Standort"
    )

    article_number = tables.Column(
        accessor="item.article_number",
        verbose_name="Artikelnummer"
    )

    responsible = tables.Column(
        accessor="item.responsible",
        verbose_name="Verantwortlicher"
    )

    status = tables.TemplateColumn(
        template_name="inventory/tables/status.html",
        verbose_name="Status"
    )

    actions = tables.TemplateColumn(
        template_name="inventory/tables/actions.html",
        verbose_name="Aktionen",
        orderable=False
    )

    class Meta:
        model = ProjectInventoryItem
        fields = (
            "name",
            "category",
            "quantity",
            "location",
            "article_number",
            "responsible",
            "status",
            "actions",
        )
        attrs = {
            "class": "w-full text-sm"
        }