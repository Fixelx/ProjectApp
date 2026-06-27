from django import forms

from .models import InventoryItem, ShoppingItem
from core.forms.base import BaseForm


class InventoryItemForm(BaseForm):

    class Meta:
        model = InventoryItem
        fields = [
            "name",
            "description",
            "quantity",
            "location",
            "article_number",
            "responsible",
            "category",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()


class ShoppingItemForm(BaseForm):

    class Meta:
        model = ShoppingItem

        fields = [
            "name",
            "description",
            "quantity",
            "supplier",
            "price",
            "category",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.apply_style()