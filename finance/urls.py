from django.urls import path
from .views import finance_overview, finance_view, add_income, add_expense

app_name = "finance"

urlpatterns = [
    path("<int:project_id>/finance/", finance_overview, name="overview"),
    path("<int:project_id>/finance/view/", finance_view, name="view"),
    path("<int:project_id>/finance/add-income/", add_income, name="add_income"),
    path("<int:project_id>/finance/add-expense/", add_expense, name="add_expense"),
]