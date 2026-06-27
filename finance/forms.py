from django import forms
from .models import Income, Expense
from core.forms.base import BaseForm
from django.utils import timezone

class IncomeForm(BaseForm):
    class Meta:
        model = Income
        fields = ["name", "amount", "date", "category", "payment_method", "note"]
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields["date"].initial = timezone.now()

        self.apply_style()


class ExpenseForm(BaseForm):
    class Meta:
        model = Expense
        fields = ["name", "amount", "date", "category", "supplier", "payment_method", "receipt", "note"]

        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields["date"].initial = timezone.now()

        self.apply_style()
