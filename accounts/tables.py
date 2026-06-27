import django_tables2 as tables
from django.contrib.auth.models import User
from .models import Role

class RoleTable(tables.Table):
    toggle_prefix = "role"
    detail_template = "accounts/tables/user/role_edit_form.html"
    name = tables.Column(
        verbose_name="Rolle"
    )

    class Meta:
        model = Role
        template_name = "django_tables2/table_toggle.html"
        fields = (
            "name",
        )
        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }

class ArchivedUserTable(tables.Table):
    toggle_prefix = "user"
    detail_template = "accounts/tables/user/archive_edit_form.html"
    username = tables.Column(
        verbose_name="Benutzername"
    )
    first_name = tables.Column(
        verbose_name="Vorname"
    )
    last_name = tables.Column(
        verbose_name="Nachname"
    )
    email = tables.Column(
        verbose_name="E-Mail"
    )
    role = tables.TemplateColumn(
        template_name="accounts/tables/user/role.html",
        verbose_name="Rolle",
        orderable=False
    )
    superuser = tables.TemplateColumn(
        template_name="accounts/tables/user/superuser.html",
        verbose_name="Superuser",
        orderable=False
    )

    class Meta:
        model = User
        template_name = "django_tables2/table_toggle.html"
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "superuser",
        )
        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }

class UserTable(tables.Table):
    toggle_prefix = "user"
    detail_template = "accounts/tables/user/edit_form.html"
    username = tables.Column(
        verbose_name="Benutzername"
    )
    first_name = tables.Column(
        verbose_name="Vorname"
    )
    last_name = tables.Column(
        verbose_name="Nachname"
    )
    email = tables.Column(
        verbose_name="E-Mail"
    )
    role = tables.TemplateColumn(
        template_name="accounts/tables/user/role.html",
        verbose_name="Rolle",
        orderable=False
    )
    superuser = tables.TemplateColumn(
        template_name="accounts/tables/user/superuser.html",
        verbose_name="Superuser",
        orderable=False
    )

    class Meta:
        model = User
        template_name = "django_tables2/table_toggle.html"
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "superuser",
        )
        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }