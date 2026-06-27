from django.urls import path
from . import views

app_name = "inventory_global"

urlpatterns = [
    path("", views.inventory_global_overview, name="overview"),
    path("add/", views.inventory_global_add, name="add"),
    path("edit/<int:item_id>/", views.inventory_global_edit, name="edit"),
    path("delete/<int:item_id>/", views.inventory_global_delete, name="delete"),
]