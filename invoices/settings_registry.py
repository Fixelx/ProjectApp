from masterdata.registry import register_setting

from .models import (
    Unit, DocumentNumberSettings
)
register_setting(
    group="Rechnungswesen",
    name="Einheiten",
    model=Unit,
)

register_setting(
    group="Rechnungswesen",
    name="Dokumentnummern",
    model=DocumentNumberSettings,
    setting_type="single",
)