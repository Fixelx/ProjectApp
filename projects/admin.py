from django.contrib import admin
from .models import Project, ProjectMembership, ProjectContact, ProjectLocation


class ProjectMembershipInline(admin.TabularInline):
    model = ProjectMembership
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "active",
        "created_at",
    )

    search_fields = (
        "name",
    )

    inlines = [
        ProjectMembershipInline
    ]


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "project",
        "role",
    )

    list_filter = (
        "role",
    )


@admin.register(ProjectContact)
class ProjectContactAdmin(admin.ModelAdmin):
    list_display = ("project", "contact", "created_at")
    search_fields = ("project__name", "contact__first_name", "contact__last_name")
    autocomplete_fields = ("project", "contact")
    list_filter = ("project",)


@admin.register(ProjectLocation)
class ProjectLocationAdmin(admin.ModelAdmin):
    list_display = ("project", "location", "created_at")
    search_fields = ("project__name", "location__name")
    autocomplete_fields = ("project", "location")
    list_filter = ("project",)