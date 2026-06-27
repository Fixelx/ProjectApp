from masterdata.registry import register_setting

from .models import (
    DocumentCategory,
)


register_setting(
    group="Dokumente",
    name="Kategorien",
    model=DocumentCategory,
)