import django_tables2 as tables
from django.utils.html import format_html

class PeriodAnalyticsTable(tables.Table):
    period = tables.Column(verbose_name="Zeitraum")
    income = tables.Column(verbose_name="Einnahmen")
    expense = tables.Column(verbose_name="Ausgaben")
    profit = tables.Column(verbose_name="Gewinn")

    actions = tables.TemplateColumn(
        template_name="finance/tables/period_actions.html",
        verbose_name="Aktionen",
        orderable=False,
    )

    class Meta:
        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }
        template_name = "django_tables2/table.html"
        fields = (
            "period",
            "income",
            "expense",
            "profit",
            "actions",
        )

    def __init__(self, *args, period_type="day", **kwargs):
        self.period_type = period_type
        super().__init__(*args, **kwargs)

    def render_period(self, value):
        if self.period_type == "year":
            return value.strftime("%Y")

        if self.period_type == "month":
            return value.strftime("%m / %Y")       # z.B. 06.2026

        if self.period_type == "week":
            week = value.isocalendar().week
            return f"KW {week:02d} / {value.year}"

        return value.strftime("%d.%m.%Y")

    def render_income(self, value):
        return f"{value:.2f} €"

    def render_expense(self, value):
        return f"{value:.2f} €"

    def render_profit(self, value):
        return f"{value:.2f} €"















class FinanceTransactionTable(tables.Table):

    type = tables.Column(
        verbose_name="Typ"
    )

    name = tables.Column(
        verbose_name="Name"
    )

    amount = tables.Column(
        verbose_name="Betrag"
    )

    date = tables.DateColumn(
        verbose_name="Datum",
        format="d.m.Y"
    )

    category = tables.Column(
        verbose_name="Kategorie"
    )

    created_by = tables.Column(
        verbose_name="Erstellt von"
    )

    payment_method = tables.Column(
        verbose_name="Zahlungsmethode"
    )

    supplier = tables.Column(
        verbose_name="Lieferant"
    )

    receipt = tables.TemplateColumn(
        template_name="finance/tables/receipt.html",
        verbose_name="Beleg",
        orderable=False,
    )

    note = tables.Column(
        verbose_name="Notiz"
    )

    class Meta:
        attrs = {
            "class": "w-full text-sm min-w-[700px]"
        }
        template_name = "django_tables2/table.html"
        fields = (
            "type",
            "name",
            "amount",
            "date",
            "category",
            "created_by",
            "payment_method",
            "supplier",
            "receipt",
            "note",
        )



    def render_type(self, value):
        color = "text-green-600" if value == "Einnahme" else "text-red-600"
        return format_html(
            '<span class="font-bold {}">{}</span>',
            color,
            value,
        )

    def render_amount(self, value):
        if value is None:
            return "/"
        return f"{value:.2f} €"

    def render_name(self, value):
        return value or "/"

    def render_category(self, value):
        return value or "/"

    def render_created_by(self, value):
        return value or "/"

    def render_payment_method(self, value):
        return value or "/"

    def render_supplier(self, value):
        return value or "/"

    def render_note(self, value):
        return value or "/"