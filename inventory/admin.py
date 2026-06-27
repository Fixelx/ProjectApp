from django.contrib import admin

from .models import (
    InventoryCategory,
    InventoryLocation,
    InventoryItem,
    ProjectInventoryItem,
    ShoppingItem,
)

@admin.register(InventoryCategory)
class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(InventoryLocation)
class InventoryLocationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "quantity",
        "category",
        "location",
        "responsible",
        "article_number",
    )
    list_filter = (
        "category",
        "location",
    )
    search_fields = (
        "name",
        "article_number",
        "description",
    )


@admin.register(ProjectInventoryItem)
class ProjectInventoryItemAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "item",
        "quantity",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "project",
    )
    search_fields = (
        "project__name",
        "item__name",
    )


@admin.register(ShoppingItem)
class ShoppingItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "project",
        "quantity",
        "price",
        "category",
        "supplier",
        "created_at",
    )
    list_filter = (
        "project",
        "category",
        "supplier",
    )
    search_fields = (
        "name",
        "description",
        "project__name",
    )