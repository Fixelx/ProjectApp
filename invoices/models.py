from django.db import models
from django.core.exceptions import ValidationError
from core.models import CompanySetting

class Unit(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Bezeichnung"
    )
    short_name = models.CharField(
        max_length=20,
        verbose_name="Kürzel"
    )
    class Meta:
        verbose_name = "Einheit"
        verbose_name_plural = "Einheiten"
        ordering = ["name"]
    def __str__(self):
        return self.name

class Customer(models.Model):
    class CustomerType(models.TextChoices):
        PRIVATE = "private", "Privat"
        COMPANY = "company", "Unternehmen"

    customer_number = models.CharField(max_length=50, unique=True, verbose_name="Kunden-ID")
    customer_type = models.CharField(max_length=20, choices=CustomerType.choices, default=CustomerType.COMPANY, verbose_name="Kundentyp")

    company_name = models.CharField(max_length=255, verbose_name="Firmenname / Kundenname")

    tax_number = models.CharField(max_length=100, blank=True, verbose_name="Steuernummer")
    vat_number = models.CharField(max_length=100, blank=True, verbose_name="UST-IdNr")

    phone = models.CharField(max_length=100, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="E-Mail")

    active = models.BooleanField(default=True, verbose_name="Status")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kunde"
        verbose_name_plural = "Kunden"
        ordering = ["company_name"]

    def __str__(self):
        return f"{self.customer_number} - {self.company_name}"


class CustomerContact(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="contacts", verbose_name="Kunde")

    first_name = models.CharField(max_length=150, verbose_name="Vorname")
    last_name = models.CharField(max_length=150, verbose_name="Nachname")

    email = models.EmailField(blank=True, verbose_name="E-Mail")
    phone = models.CharField(max_length=100, blank=True, verbose_name="Telefon")

    class Meta:
        verbose_name = "Ansprechpartner"
        verbose_name_plural = "Ansprechpartner"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CustomerLocation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="locations", verbose_name="Kunde")

    name = models.CharField(max_length=255, verbose_name="Bezeichnung")

    zip_code = models.CharField(max_length=20, blank=True, verbose_name="PLZ")
    city = models.CharField(max_length=255, blank=True, verbose_name="Ort")
    street = models.CharField(max_length=255, blank=True, verbose_name="Adresse")
    country = models.CharField(max_length=100, blank=True, verbose_name="Land")

    class Meta:
        verbose_name = "Standort"
        verbose_name_plural = "Standorte"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Item(models.Model):
    class ItemType(models.TextChoices):
        SERVICE = "service", "Dienstleistung"
        PRODUCT = "product", "Ware"

    item_type = models.CharField(max_length=20, choices=ItemType.choices, default=ItemType.PRODUCT, verbose_name="Art")
    description = models.CharField(max_length=255, verbose_name="Beschreibung")
    unit = models.ForeignKey(Unit,on_delete=models.PROTECT,related_name="item_items",verbose_name="Einheit")
  
    price_net = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preis Netto")
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=19.00,
        verbose_name="MwSt. Satz (%)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Posten"
        verbose_name_plural = "Posten"
        ordering = ["description"]

    def __str__(self):
        return self.description















class Invoice(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Entwurf"
        SENT = "sent", "Versendet"
        PAID = "paid", "Bezahlt"
        OVERDUE = "overdue", "Überfällig"
        CANCELED = "canceled", "Storniert"

    invoice_number = models.CharField(max_length=50,verbose_name="Rechnungsnummer", blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="invoices", null=True, blank=True, verbose_name="Kunde")
    project = models.ForeignKey("projects.Project", on_delete=models.SET_NULL, null=True, blank=True, related_name="invoices", verbose_name="Projekt")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name="Status")
    issue_date = models.DateField(verbose_name="Rechnungsdatum")
    due_date = models.DateField(null=True, blank=True, verbose_name="Fälligkeitsdatum")
    note = models.TextField(blank=True, verbose_name="Notiz")
    created_at = models.DateTimeField(auto_now_add=True)

    pdf_file = models.FileField(upload_to="invoice_pdfs/",null=True,blank=True,verbose_name="PDF")
    pdf_generated_at = models.DateTimeField(null=True,blank=True,verbose_name="PDF erstellt am")

    cancel_number = models.CharField(max_length=50,unique=True,null=True,blank=True,verbose_name="Stornorechnungsnummer")
    pdf_canceled_file = models.FileField(upload_to="invoice_pdfs/",null=True,blank=True,verbose_name="Stornorechnung")
    pdf_canceled_generated_at = models.DateTimeField(null=True,blank=True,verbose_name="Stornorechnung erstellt am")

    tax_number = models.CharField(max_length=100, blank=True, verbose_name="Steuernummer Kunde")
    vat_number = models.CharField(max_length=100, blank=True, verbose_name="USt-IdNr Kunde")
    contact_name = models.CharField(max_length=255, verbose_name="Ansprechpartner")
    contact_email = models.EmailField(blank=True, verbose_name="E-Mail Ansprechpartner")
    contact_phone = models.CharField(max_length=100, blank=True, verbose_name="Telefon Ansprechpartner")
    location_name = models.CharField(max_length=255, verbose_name="Standort")
    location_street = models.CharField(max_length=255, blank=True, verbose_name="Straße")
    location_city = models.CharField(max_length=255, blank=True, verbose_name="Ort")
    location_zip = models.CharField(max_length=20, blank=True, verbose_name="PLZ")
    location_country = models.CharField(max_length=100, blank=True, verbose_name="Land")

    class Meta:
        verbose_name = "Rechnung"
        verbose_name_plural = "Rechnungen"
        ordering = ["-issue_date"]

    def save(self, *args, **kwargs):

        if self.pk:

            old = Invoice.objects.get(pk=self.pk)

            if old.status in [
                self.Status.SENT,
                self.Status.PAID,
                self.Status.CANCELED,
            ]:

                protected_fields = [
                    field.name
                    for field in self._meta.fields
                    if field.name not in [
                        "status",
                        "pdf_file",
                        "pdf_generated_at",
                        "created_at",
                        "pdf_canceled_file",
                        "pdf_canceled_generated_at",
                        "cancel_number",
                    ]
                ]

                for field in protected_fields:

                    if getattr(old, field) != getattr(self, field):

                        raise ValidationError(
                            "Eine finale Rechnung kann nicht mehr bearbeitet werden."
                        )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE,related_name="items",verbose_name="Rechnung")
    source_type = models.CharField(max_length=20,choices=[("item","Artikel"),("time","Zeiterfassung"),("expense","Ausgabe"),],default="item",verbose_name="Quelle",)
    item = models.ForeignKey(Item,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Artikel") # Quelle 1
    time_entry = models.ForeignKey("time_tracking.TimeEntry",on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Zeiterfassung") # Quelle 2
    expense = models.ForeignKey("finance.Expense",on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Ausgabe") # Quelle 3
    description = models.CharField(max_length=255,verbose_name="Beschreibung")
    quantity = models.DecimalField(max_digits=10,decimal_places=2,default=1,verbose_name="Menge")
    unit = models.CharField(max_length=50,verbose_name="Einheit")
    unit_price_net = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Einzelpreis Netto")
    unit_tax_rate = models.DecimalField(max_digits=5,decimal_places=2,default=19.00,verbose_name="MwSt. Satz (%)")
    service_period_from = models.DateField(null=True,blank=True,verbose_name="Leistungszeitraum von",)
    service_period_to = models.DateField(null=True,blank=True,verbose_name="Leistungszeitraum bis",)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def calculated_total_net(self):
        return self.quantity * self.unit_price_net

    class Meta:
        verbose_name = "Rechnungsposition"
        verbose_name_plural = "Rechnungspositionen"

    def clean(self):

        sources = [
            self.item,
            self.time_entry,
            self.expense,
        ]

        selected = sum(1 for s in sources if s)

        if selected != 1:
            raise ValidationError(
                "Genau eine Quelle muss ausgewählt werden."
            )

    def __str__(self):
        return self.description
        





















class Reminder(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Entwurf"
        SENT = "sent", "Versendet"
        PAID = "paid", "Bezahlt"
        #PARTIALLY_PAID = "partial", "Teilweise bezahlt"
        CANCELED = "canceled", "Storniert"
        EXPIRED = "expired", "Frist abgelaufen"

    invoice = models.ForeignKey("Invoice",on_delete=models.PROTECT,related_name="reminders",verbose_name="Rechnung")
    reminder_number = models.CharField(max_length=50,verbose_name="Mahnungsnummer", blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Status",
    )
    level = models.PositiveSmallIntegerField(default=1,verbose_name="Mahnstufe",help_text="1 = Erste Mahnung, 2 = Zweite Mahnung, 3 = Letzte Mahnung",)
    issue_date = models.DateField(verbose_name="Mahndatum",)
    due_date = models.DateField(null=True,blank=True,verbose_name="Neue Zahlungsfrist",)
    fee = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name="Mahngebühr",)
    note = models.TextField(blank=True,verbose_name="Hinweis",)
    pdf_file = models.FileField(upload_to="reminder_pdfs/",null=True,blank=True,verbose_name="PDF",)
    pdf_generated_at = models.DateTimeField(null=True,blank=True,verbose_name="PDF erstellt am",)
    created_at = models.DateTimeField(auto_now_add=True,)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Mahnung"
        verbose_name_plural = "Mahnungen"

    def __str__(self):
        return self.reminder_number




























class Offer(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Entwurf"
        SENT = "sent", "Versendet"
        ACCEPTED = "accepted", "Akzeptiert"
        REJECTED = "rejected", "Abgelehnt"
        EXPIRED = "expired", "Ausgelaufen"

    offer_number = models.CharField(max_length=50,verbose_name="Angebotsnummer", blank=True)




    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="offers",
        null=True,
        blank=True,
        verbose_name="Kunde",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Status",
    )

    issue_date = models.DateField(
        verbose_name="Angebotsdatum",
    )

    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Gültig bis",
    )

    note = models.TextField(
        blank=True,
        verbose_name="Notiz",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    pdf_file = models.FileField(
        upload_to="offer_pdfs/",
        null=True,
        blank=True,
        verbose_name="PDF",
    )

    pdf_generated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="PDF erstellt am",
    )

    tax_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Steuernummer Kunde",
    )

    vat_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="USt-IdNr Kunde",
    )

    contact_name = models.CharField(
        max_length=255,
        verbose_name="Ansprechpartner",
    )

    contact_email = models.EmailField(
        blank=True,
        verbose_name="E-Mail Ansprechpartner",
    )

    contact_phone = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Telefon Ansprechpartner",
    )

    location_name = models.CharField(
        max_length=255,
        verbose_name="Standort",
    )

    location_street = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Straße",
    )

    location_city = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Ort",
    )

    location_zip = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="PLZ",
    )

    location_country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Land",
    )

    class Meta:
        verbose_name = "Angebot"
        verbose_name_plural = "Angebote"
        ordering = ["-issue_date"]

    def save(self, *args, **kwargs):

        if self.pk:

            old = Offer.objects.get(pk=self.pk)

            if old.status in [
                self.Status.ACCEPTED,
                self.Status.REJECTED,
                self.Status.EXPIRED,
            ]:

                protected_fields = [
                    field.name
                    for field in self._meta.fields
                    if field.name not in [
                        "status",
                        "pdf_file",
                        "pdf_generated_at",
                    ]
                ]

                for field in protected_fields:

                    if getattr(old, field) != getattr(self, field):

                        raise ValidationError(
                            "Ein finales Angebot kann nicht mehr bearbeitet werden."
                        )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.offer_number


class OfferItem(models.Model):
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Angebot",
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Artikel",
    )

    description = models.CharField(
        max_length=255,
        verbose_name="Beschreibung",
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1,
        verbose_name="Menge",
    )

    unit = models.CharField(
        max_length=50,
        verbose_name="Einheit",
    )

    unit_price_net = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Einzelpreis Netto",
    )

    unit_tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=19.00,
        verbose_name="MwSt. Satz (%)",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def calculated_total_net(self):
        return self.quantity * self.unit_price_net

    class Meta:
        verbose_name = "Angebotsposition"
        verbose_name_plural = "Angebotspositionen"

    def __str__(self):
        return self.description


























        



class DocumentNumberSettings(models.Model):
    company = models.OneToOneField(CompanySetting,on_delete=models.CASCADE,related_name="number_settings",verbose_name="Unternehmen")
    invoice_format = models.CharField(max_length=100,default="RE-{year}-{number}",verbose_name="Rechnungsformat")
    invoice_next_number = models.PositiveIntegerField(default=1,verbose_name="Rechnungs ID (nächste)")
    cancel_format = models.CharField(max_length=100,default="ST-{year}-{number}",verbose_name="Stornoformat")
    cancel_next_number = models.PositiveIntegerField(default=1,verbose_name="Storno ID (nächste)")
    offer_format = models.CharField(max_length=100,default="ANG-{year}-{number}",verbose_name="Angebotsformat")
    offer_next_number = models.PositiveIntegerField(default=1,verbose_name="Angebots ID (nächste)")
    reminder_format = models.CharField(max_length=100,default="M-{year}-{number}",verbose_name="Mahnungsformat")
    reminder_next_number = models.PositiveIntegerField(default=1,verbose_name="Mahnungs ID (nächste)")

    class Meta:
        verbose_name = "Dokumentnummer"
        verbose_name_plural = "Dokumentnummern"
