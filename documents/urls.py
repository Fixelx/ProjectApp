from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("<int:project_id>/documents/", views.document_overview, name="overview"),
    path("<int:project_id>/documents/delete/<int:doc_id>/", views.document_delete, name="delete"),
    path("<int:project_id>/documents/add/", views.document_add, name="add"),
]