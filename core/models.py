from django.db import models


class CompanySetting(models.Model):
    companyname = models.CharField(max_length=255,verbose_name="Firmenname")
    name = models.CharField(max_length=255,verbose_name="Geschäftsführer")
    logo = models.ImageField(upload_to="company/",blank=True,null=True,verbose_name="Logo")
    slogan = models.CharField(max_length=255,blank=True,verbose_name="Slogan")
    color = models.CharField(max_length=20,default="#0f172a",verbose_name="Farbe")
    street = models.CharField(max_length=255,verbose_name="Straße")
    zip = models.CharField(max_length=20,verbose_name="PLZ")
    city = models.CharField(max_length=255,verbose_name="Ort")
    country = models.CharField(max_length=100,default="Deutschland",verbose_name="Land")
    phone = models.CharField(max_length=100,blank=True,verbose_name="Telefon"    )
    email = models.EmailField(max_length=100,blank=True,verbose_name="E-Mail")
    website = models.URLField(max_length=100,blank=True,verbose_name="Webseite")

    tax_number = models.CharField(max_length=100,blank=True,verbose_name="Steuernummer")
    vat_number = models.CharField(max_length=100,blank=True,verbose_name="USt-IdNr.")

    is_small_business = models.BooleanField(default=False,verbose_name="Kleinunternehmer (§19 UStG)")
    small_business_text = models.TextField(blank=True,verbose_name="Kleinunternehmer Hinweis")
    invoice_header_text = models.TextField(blank=True,verbose_name="Rechnungszusatztext")
    offer_header_text = models.TextField(blank=True,verbose_name="Angebotszusatztext")
    reminder_header_text = models.TextField(blank=True,verbose_name="Mahnungszusatztext")

    bank_name = models.CharField(max_length=255,blank=True,verbose_name="Bank")
    iban = models.CharField(max_length=50,blank=True,verbose_name="IBAN")
    bic = models.CharField(max_length=50,blank=True,verbose_name="BIC")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Firmeneinstellung"
        verbose_name_plural = "Firmeneinstellungen"


    def __str__(self):
        return self.name

