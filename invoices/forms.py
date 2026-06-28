from django import forms
from core.forms.base import BaseForm
from .models import Customer, Item, Invoice, InvoiceItem, CustomerContact, CustomerLocation, Offer, OfferItem, Reminder, InvoicePayment
from projects.models import Project
from time_tracking.models import TimeEntry
from finance.models import Expense
from django.utils import timezone
from django.db.models import Q, Max



class InvoicePaymentForm(BaseForm):
    class Meta:
        model = InvoicePayment
        fields = [
            "amount",
            "date",
            "payment_method",
            "note",
        ]

        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].initial = timezone.now().date()
        self.apply_style()




class CustomerForm(BaseForm):
    class Meta:
        model = Customer
        fields = [
            "customer_number",
            "customer_type",
            "company_name",
            "tax_number",
            "vat_number",
            "phone",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()



class ItemForm(BaseForm):
    class Meta:
        model = Item
        fields = [
            "item_type",
            "description",
            "category",
            "unit",
            "price_net",
            "tax_rate",
            "price_buy",
            "supplier",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()





class CustomerInvoiceForm(BaseForm):

    contact = forms.ModelChoiceField(
        queryset=CustomerContact.objects.none(),
        label="Ansprechpartner",
        required=True
    )

    location = forms.ModelChoiceField(
        queryset=CustomerLocation.objects.none(),
        label="Standort",
        required=True
    )

    class Meta:
        model = Invoice
        fields = [
            "customer",
            "contact",
            "location",
            "issue_date",
            "due_date",
            "note",
        ]

        widgets = {
            "issue_date": forms.DateInput(attrs={"type": "date"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

        customer_id = (
            self.data.get("customer")
            or getattr(self.instance, "customer_id", None)
        )

        if customer_id:
            self.fields["contact"].queryset = CustomerContact.objects.filter(customer_id=customer_id)
            self.fields["location"].queryset = CustomerLocation.objects.filter(customer_id=customer_id)
        else:
            self.fields["contact"].queryset = CustomerContact.objects.none()
            self.fields["location"].queryset = CustomerLocation.objects.none()





class ProjectInvoiceForm(BaseForm):

    contact = forms.ModelChoiceField(
        queryset=CustomerContact.objects.none(),
        required=False,
        label="Ansprechpartner",
        widget=forms.Select(attrs={
            "class": "customer-field"
        })
    )

    location = forms.ModelChoiceField(
        queryset=CustomerLocation.objects.none(),
        required=False,
        label="Standort",
        widget=forms.Select(attrs={
            "class": "customer-field"
        })
    )


    contact_name_manual = forms.CharField(
        required=False,
        label="Ansprechpartner",
        widget=forms.TextInput(attrs={
            "class": "manual-field"
        })
    )

    contact_email_manual = forms.EmailField(
        required=False,
        label="E-Mail",
        widget=forms.EmailInput(attrs={
            "class": "manual-field"
        })
    )

    contact_phone_manual = forms.CharField(
        required=False,
        label="Telefon",
        widget=forms.TextInput(attrs={
            "class": "manual-field"
        })
    )


    location_name_manual = forms.CharField(
        required=False,
        label="Standort",
        widget=forms.TextInput(attrs={
            "class": "manual-field"
        })
    )

    location_street_manual = forms.CharField(
        required=False,
        label="Straße",
        widget=forms.TextInput(attrs={
            "class": "manual-field"
        })
    )

    location_zip_manual = forms.CharField(
        required=False,
        label="PLZ",
        widget=forms.TextInput(attrs={
            "class": "manual-field"
        })
    )

    location_city_manual = forms.CharField(
        required=False,
        label="Ort",
        widget=forms.TextInput(attrs={
            "class": "manual-field"
        })
    )

    location_country_manual = forms.CharField(
        required=False,
        label="Land",
        widget=forms.TextInput(attrs={
            "class": "manual-field"
        })
    )


    class Meta:

        model = Invoice

        fields = [
            "project",

            "contact",
            "location",

            "contact_name_manual",
            "contact_email_manual",
            "contact_phone_manual",

            "location_name_manual",
            "location_street_manual",
            "location_zip_manual",
            "location_city_manual",
            "location_country_manual",

            "issue_date",
            "due_date",
            "note",
        ]


        widgets = {

            "issue_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "due_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
        }

    



    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.apply_style()


        project_id = self.data.get("project") or getattr(
            self.instance,
            "project_id",
            None
        )


        if project_id:

            project = Project.objects.filter(
                id=project_id
            ).first()


            if project and project.customer:

                self.fields["contact"].queryset = CustomerContact.objects.filter(
                    customer=project.customer
                )

                self.fields["location"].queryset = CustomerLocation.objects.filter(
                    customer=project.customer
                )





class InvoiceItemForm(BaseForm):

    class Meta:
        model = InvoiceItem

        fields = [
            "source_type",
            "item",
            "time_entry",
            "expense",
            "description",
            "quantity",
            "unit",
            "unit_price_net",
            "unit_tax_rate",
            'service_period_from',
            'service_period_to',
        ]
        widgets = {

            "quantity": forms.NumberInput(attrs={
                "step": "1.00"
            }),

            "unit_price_net": forms.NumberInput(attrs={
                "step": "1.00"
            }),

            "unit_tax_rate": forms.NumberInput(attrs={
                "step": "1.00"
            }),
                        "issue_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "service_period_from": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "service_period_to": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
            
        }


    def __init__(
        self,
        *args,
        invoice=None,
        **kwargs
    ):

        super().__init__(*args, **kwargs)
        self.apply_style()
        self.invoice = invoice
        self.fields["item"].queryset = Item.objects.all()
        self.fields["time_entry"].queryset = TimeEntry.objects.none()
        self.fields["expense"].queryset = Expense.objects.none()


        if invoice and invoice.project:


            self.fields["source_type"].choices = [
                ("item", "Artikel"),
                ("time", "Zeiterfassung"),
                ("expense", "Ausgabe"),
            ]


            self.fields["time_entry"].queryset = TimeEntry.objects.filter(
                project=invoice.project,end__isnull=False
            )


            self.fields["expense"].queryset = Expense.objects.filter(
                project=invoice.project
            )

        else:
            self.fields["source_type"].choices = [
                ("item", "Artikel"),
            ]

        self.fields["item"].widget.attrs["class"] += " source-item"
        self.fields["time_entry"].widget.attrs["class"] += " source-time"
        self.fields["expense"].widget.attrs["class"] += " source-expense"

    def save(self, commit=True):

        obj = super().save(commit=False)


        source = self.cleaned_data.get(
            "source_type"
        )


        # -------------------------
        # ARTIKEL
        # -------------------------

        if source == "item":

            item = self.cleaned_data["item"]

            obj.item = item
            obj.time_entry = None
            obj.expense = None

            obj.description = self.cleaned_data["description"]
            obj.unit = self.cleaned_data["unit"]
            obj.unit_price_net = self.cleaned_data["unit_price_net"]
            obj.unit_tax_rate = self.cleaned_data["unit_tax_rate"]



        # -------------------------
        # ZEITERFASSUNG
        # -------------------------

        elif source == "time":

            entry = self.cleaned_data["time_entry"]

            obj.item = None
            obj.time_entry = entry
            obj.expense = None


            obj.description = self.cleaned_data["description"]
            obj.unit = self.cleaned_data["unit"]
            obj.unit_price_net = self.cleaned_data["unit_price_net"]
            obj.unit_tax_rate = self.cleaned_data["unit_tax_rate"]



        # -------------------------
        # AUSGABE
        # -------------------------

        elif source == "expense":

            expense = self.cleaned_data["expense"]

            obj.item = None
            obj.time_entry = None
            obj.expense = expense


            obj.description = self.cleaned_data["description"]
            obj.unit = self.cleaned_data["unit"]
            obj.unit_price_net = self.cleaned_data["unit_price_net"]
            obj.unit_tax_rate = self.cleaned_data["unit_tax_rate"]



        if commit:
            obj.save()


        return obj

























class OfferForm(BaseForm):

    contact = forms.ModelChoiceField(
        queryset=CustomerContact.objects.none(),
        label="Ansprechpartner",
        required=True
    )

    location = forms.ModelChoiceField(
        queryset=CustomerLocation.objects.none(),
        label="Standort",
        required=True
    )

    class Meta:
        model = Offer
        fields = [
            "customer",
            "contact",
            "location",
            "issue_date",
            "due_date",
            "note",
        ]

        widgets = {
            "issue_date": forms.DateInput(attrs={"type": "date"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

        customer_id = (
            self.data.get("customer")
            or getattr(self.instance, "customer_id", None)
        )

        if customer_id:
            self.fields["contact"].queryset = CustomerContact.objects.filter(customer_id=customer_id)
            self.fields["location"].queryset = CustomerLocation.objects.filter(customer_id=customer_id)
        else:
            self.fields["contact"].queryset = CustomerContact.objects.none()
            self.fields["location"].queryset = CustomerLocation.objects.none()





class OfferItemForm(BaseForm):

    class Meta:
        model = OfferItem

        fields = [
            "item",
            "description",
            "quantity",
            "unit",
            "unit_price_net",
            "unit_tax_rate",
        ]

        widgets = {
            "quantity": forms.NumberInput(
                attrs={"step": "1.00"}
            ),
            "unit_price_net": forms.NumberInput(
                attrs={"step": "1.00"}
            ),
            "unit_tax_rate": forms.NumberInput(
                attrs={"step": "1.00"}
            ),
        }

    def __init__(
        self,
        *args,
        offer=None,
        **kwargs
    ):

        super().__init__(*args, **kwargs)

        self.apply_style()

        self.offer = offer

        self.fields["item"].queryset = (
            Item.objects.all()
        )

    def save(self, commit=True):

        obj = super().save(commit=False)

        item = self.cleaned_data.get("item")

        if item:
            obj.item = item

        if commit:
            obj.save()

        return obj








class ReminderForm(BaseForm):

    class Meta:
        model = Reminder
        fields = [
            "invoice",
            "issue_date",
            "due_date",
            "fee",
            "note",
        ]

        widgets = {
            "issue_date": forms.DateInput(attrs={"type": "date"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        possible_invoices = []


        invoices = Invoice.objects.filter(
            status=Invoice.Status.OVERDUE,
            due_date__lt=timezone.now().date(),
        ).prefetch_related(
            "reminders"
        )


        for invoice in invoices:

            reminders = invoice.reminders.exclude(
                status=Reminder.Status.CANCELED
            ).order_by("-level")


            # Keine Mahnung vorhanden
            if not reminders.exists():
                possible_invoices.append(invoice)
                continue


            last_reminder = reminders.first()


            # Nur nach expired möglich
            if last_reminder.status != Reminder.Status.EXPIRED:
                continue


            # Maximal 3 Mahnungen
            if last_reminder.level >= 3:
                continue


            possible_invoices.append(invoice)


        self.fields["invoice"].queryset = Invoice.objects.filter(
            id__in=[i.id for i in possible_invoices]
        ).order_by("due_date")


        self.apply_style()