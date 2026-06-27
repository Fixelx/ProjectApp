from django.contrib import admin
from .models import TimeEntry


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "user",
        "entry_type",
        "activity",
        "start",
        "end",
        "break_minutes",
    )

    list_filter = (
        "entry_type",
        "project",
        "user",
    )

    search_fields = (
        "activity",
        "project__name",
        "user__username",
        "user__first_name",
        "user__last_name",
    )

    autocomplete_fields = (
        "project",
        "user",
    )

    ordering = (
        "-start",
    )