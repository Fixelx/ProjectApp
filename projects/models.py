from django.db import models
from django.contrib.auth import get_user_model
from invoices.models import Customer, CustomerContact, CustomerLocation
import os

User = get_user_model()

def logo_upload_path(instance, filename):
    return f"projects/{instance.id}/logo/{filename}"

class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    logo = models.ImageField(upload_to=logo_upload_path, blank=True, null=True, verbose_name="Logo")
    color = models.CharField(max_length=20, default="#2563eb", verbose_name="Farbe")
    icon = models.CharField(max_length=100, blank=True, verbose_name="Icon")
    active = models.BooleanField(default=True, verbose_name="Status")
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="projects",
        verbose_name="Kunde"
    )
    hourly_rate = models.DecimalField(max_digits=10,decimal_places=2,default=25,verbose_name="Stundenlohn")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        customer_changed = False

        if self.pk:
            old_customer_id = (
                Project.objects
                .filter(pk=self.pk)
                .values_list("customer_id", flat=True)
                .first()
            )

            customer_changed = old_customer_id != self.customer_id

        super().save(*args, **kwargs)

        if customer_changed:
            self.project_contacts.all().delete()
            self.project_locations.all().delete()

    def __str__(self):
        return self.name


class ProjectMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Eigentümer"
        MANAGER = "manager", "Manager"
        EMPLOYEE = "employee", "Mitarbeiter"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_memberships")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.EMPLOYEE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.user} - {self.project} ({self.role})"


class ProjectContact(models.Model):
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="project_contacts",
        verbose_name="Projekt"
    )

    contact = models.ForeignKey(
        CustomerContact,
        on_delete=models.CASCADE,
        related_name="project_links",
        verbose_name="Ansprechpartner"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")

    def clean(self):
        super().clean()

        if not self.project_id or not self.location_id:
            return

        if self.location.customer_id != self.project.customer_id:
            raise ValidationError({
                "location": "Der Ansprechpartner gehört nicht zum Kunden des Projekts."
            })

    class Meta:
        unique_together = ("project", "contact")


class ProjectLocation(models.Model):
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="project_locations",
        verbose_name="Projekt"
    )

    location = models.ForeignKey(
        CustomerLocation,
        on_delete=models.CASCADE,
        related_name="project_links",
        verbose_name="Standort"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")

    def clean(self):
        super().clean()

        if not self.project_id or not self.location_id:
            return

        if self.location.customer_id != self.project.customer_id:
            raise ValidationError({
                "location": "Der Standort gehört nicht zum Kunden des Projekts."
            })

    class Meta:
        unique_together = ("project", "location")