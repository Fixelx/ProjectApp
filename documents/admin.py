from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import DocumentCategory, Document


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "category",
        "uploaded_by",
        "created_at",
    )

    list_filter = (
        "project",
        "category",
        "created_at",
    )

    search_fields = (
        "title",
    )

    readonly_fields = (
        "created_at",
    )

    autocomplete_fields = (
        "project",
        "category",
        "uploaded_by",
    )

    ordering = (
        "-created_at",
    )