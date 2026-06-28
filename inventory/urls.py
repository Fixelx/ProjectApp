from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("<int:project_id>/inventory/", views.inventory_overview, name="overview"),
    path("<int:project_id>/inventory/add/", views.inventory_add, name="add"),
    path("<int:project_id>/inventory/shopping-add/", views.shopping_add, name="shopping_add"),

    path("<int:project_id>/inventory/edit/<int:item_id>/", views.inventory_edit, name="edit"),
    path("<int:project_id>/inventory/shopping-edit/<int:item_id>/", views.shopping_edit, name="shopping_edit"),

    path("<int:project_id>/inventory/delete/<int:item_id>/", views.inventory_delete, name="delete"),
    path("<int:project_id>/inventory/shopping-delete/<int:item_id>/", views.shopping_delete, name="shopping_delete"),

    path("<int:project_id>/inventory/shopping-to-expense/", views.shopping_to_expense, name="shopping_to_expense"),
]