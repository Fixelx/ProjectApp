from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("add/", views.project_add, name="add"),
    path("archived/", views.projects_archived, name="archived"),
    path("<int:project_id>/", views.project_overview, name="overview"),
    path("<int:project_id>/info/", views.project_info, name="info"),
    path("<int:project_id>/info/edit/",views.project_edit,name="edit"),
    path("<int:project_id>/info/contact/add/", views.project_contact_add, name="contact_add"),
    path("<int:project_id>/info/contact/<int:contact_id>/delete/", views.project_contact_delete, name="contact_delete"),
    path("<int:project_id>/info/location/add/", views.project_location_add, name="location_add"),
    path("<int:project_id>/info/location/<int:location_id>/delete/", views.project_location_delete, name="location_delete"),
    path("<int:project_id>/info/worker/add/", views.project_worker_add, name="worker_add"),
    path("<int:project_id>/info/worker/<int:worker_id>/delete/", views.project_worker_delete, name="worker_delete"),
]