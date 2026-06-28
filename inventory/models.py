from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from finance.models import Category, Supplier
from django.db.models import Sum
from django.core.validators import MinValueValidator

class InventoryCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Name")

    class Meta:
        verbose_name = "Inventarkategorie"
        verbose_name_plural = "Inventarkategorien"
        ordering = ["name"]

    def __str__(self):
        return self.name


class InventoryLocation(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Name")

    class Meta:
        verbose_name = "Inventarstandort"
        verbose_name_plural = "Inventarstandorte"
        ordering = ["name"]

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Beschreibung")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Anzahl", validators=[MinValueValidator(0,message="Die Anzahl darf nicht negativ sein.")])
    location = models.ForeignKey(InventoryLocation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Standort")
    article_number = models.CharField(max_length=255, blank=True, verbose_name="Artikelnummer")
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Verantwortlicher")
    category = models.ForeignKey(InventoryCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kategorie")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Inventarartikel"
        verbose_name_plural = "Inventarartikel"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ProjectInventoryItem(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Offen"
        PACKED = "packed", "Eingepackt"
        ON_SITE = "on_site", "Vor Ort"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="inventory_items", verbose_name="Projekt")
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, verbose_name="Artikel")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Anzahl", validators=[MinValueValidator(0,message="Die Anzahl darf nicht negativ sein.")])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Projektartikel"
        verbose_name_plural = "Projektartikel"
        unique_together = ("project", "item")

    def __str__(self):
        return f"{self.project} - {self.item}"


class ShoppingItem(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="shopping_items", verbose_name="Projekt")
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Beschreibung")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Anzahl", validators=[MinValueValidator(0,message="Die Anzahl darf nicht negativ sein.")])
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Lieferant")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preis",validators=[MinValueValidator(0,message="Der Betrag darf nicht negativ sein.")])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kategorie")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Einkaufslistenartikel"
        verbose_name_plural = "Einkaufslistenartikel"
        ordering = ["name"]

    def __str__(self):
        return self.name