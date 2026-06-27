from masterdata.registry import register_setting
from .models import CompanySetting


register_setting(
    group="System",
    name="Firmeneinstellungen",
    model=CompanySetting,
    setting_type="single",
)