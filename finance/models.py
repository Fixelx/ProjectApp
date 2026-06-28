from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project
import os
from django.core.validators import MinValueValidator



User = get_user_model()

def receipt_upload_path(instance, filename): 
    return f"projects/{instance.project.id}/receipts/{filename}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Finanzkategorie"
        verbose_name_plural = "Finanzkategorien"

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=150)
    class Meta:
        verbose_name = "Lieferant"
        verbose_name_plural = "Lieferanten"

    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name = "Zahlungsmethode"
        verbose_name_plural = "Zahlungsmethoden"

    def __str__(self):
        return self.name

class Expense(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="expenses", verbose_name="Projekt")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Kategorie")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Lieferant")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Erstellt von")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name="Zahlungsmethode")
    amount = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Betrag (€)",validators=[MinValueValidator(0,message="Der Betrag darf nicht negativ sein.")])
    date = models.DateTimeField(verbose_name="Datum")
    receipt = models.FileField(upload_to=receipt_upload_path, null=True, blank=True, verbose_name="Beleg")
    note = models.TextField(blank=True, verbose_name="Notiz")
    invoiced = models.BooleanField(default=False,verbose_name="Abgerechnet")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    def __str__(self):
        return f"{self.name} - {self.amount} €"

class Income(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name", null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="incomes", verbose_name="Projekt")
    invoice = models.OneToOneField(
        "invoices.Invoice",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="income"
    )

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Kategorie")
    amount = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Betrag (€)",validators=[MinValueValidator(0,message="Der Betrag darf nicht negativ sein.")])
    date = models.DateTimeField(verbose_name="Datum")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Erstellt von")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name="Zahlungsmethode")
    note = models.TextField(blank=True, verbose_name="Notiz")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    def __str__(self):
        return f"+{self.amount} € - {self.project.name}"