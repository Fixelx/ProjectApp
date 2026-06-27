from .models import Document
from core.forms.base import BaseForm

class DocumentForm(BaseForm):
    class Meta:
        model = Document
        fields = ["title", "category", "file"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()