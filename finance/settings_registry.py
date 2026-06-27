from masterdata.registry import register_setting

from .models import (
    Category,
    Supplier,
    PaymentMethod,
)


register_setting(
    group="Finanzen",
    name="Kategorien",
    model=Category,
)

register_setting(
    group="Finanzen",
    name="Lieferanten",
    model=Supplier,
)

register_setting(
    group="Finanzen",
    name="Zahlungsarten",
    model=PaymentMethod,
)