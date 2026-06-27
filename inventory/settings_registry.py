from masterdata.registry import register_setting

from .models import (
    InventoryCategory,
    InventoryLocation,
)


register_setting(
    group="Inventar",
    name="Kategorien",
    model=InventoryCategory,
)

register_setting(
    group="Inventar",
    name="Standorte",
    model=InventoryLocation,
)