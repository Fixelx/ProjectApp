from django import forms
from django.contrib.auth.models import User
from .models import Role
from core.forms.base import BaseForm

class UserAddForm(BaseForm):

    password = forms.CharField(
        label="Passwort",
        widget=forms.PasswordInput
    )

    role = forms.ModelChoiceField(
        queryset=Role.objects.order_by("name"),
        required=False,
        label="Rolle"
    )

    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]

        labels = {
            "username": "Benutzername",
            "first_name": "Vorname",
            "last_name": "Nachname",
            "email": "E-Mail",
        }

        help_texts = {
            "username": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()


class RoleForm(BaseForm):

    class Meta:
        model = Role

        fields = [
            "name",
        ]

        labels = {
            "name": "Rollenname",
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()