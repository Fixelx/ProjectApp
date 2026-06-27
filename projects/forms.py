from django import forms
from core.forms.base import BaseForm
from invoices.models import CustomerContact, CustomerLocation
from .models import ProjectContact, ProjectLocation, Project, ProjectMembership
from django.contrib.auth import get_user_model
User = get_user_model()

class ProjectAddForm(BaseForm):
    class Meta:
        model = Project
        fields = [
            "name",
            "customer",
            "logo",
            "color",
            "icon",
            "hourly_rate",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

class ProjectForm(BaseForm):
    class Meta:
        model = Project
        fields = [
            "name",
            "logo",
            "color",
            "icon",
            "hourly_rate",
            "active"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

class ProjectAddContactForm(BaseForm):
    class Meta:
        model = ProjectContact
        fields = ["contact"]

    def __init__(self, *args, **kwargs):
        project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)

        qs = CustomerContact.objects.none()

        if project and project.customer:
            qs = CustomerContact.objects.filter(
                customer=project.customer
            ).exclude(
                project_links__project=project
            )

        self.fields["contact"].queryset = qs
        self.apply_style()

class ProjectAddLocationForm(BaseForm):
    class Meta:
        model = ProjectLocation
        fields = ["location"]

    def __init__(self, *args, **kwargs):
        project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)

        qs = CustomerLocation.objects.none()

        if project and project.customer:
            qs = CustomerLocation.objects.filter(
                customer=project.customer
            ).exclude(
                project_links__project=project
            )

        self.fields["location"].queryset = qs
        self.apply_style()


class ProjectAddWorkerForm(BaseForm):

    class Meta:
        model = ProjectMembership

        fields = [
            "user",
            "role",
        ]

    def __init__(self, *args, project=None, **kwargs):

        super().__init__(*args, **kwargs)

        self.apply_style()

        if project:
            self.fields["user"].queryset = User.objects.exclude(
                project_memberships__project=project
            )