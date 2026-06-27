from django.contrib import admin
from .models import Category, Supplier, PaymentMethod, Expense, Income


admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(PaymentMethod)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("amount", "project", "category", "date", "created_by")
    list_filter = ("project", "category", "date")
    search_fields = (
        "name",
        "project__name",
    )


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("amount", "project", "category", "date", "created_by")
    list_filter = ("project", "category", "date")