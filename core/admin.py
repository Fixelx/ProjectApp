from django.contrib import admin
from .models import CompanySetting


@admin.register(CompanySetting)
class CompanySettingAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "city",
        "updated_at",
    )