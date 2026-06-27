from django.urls import path
from . import views

app_name = "time_tracking"

urlpatterns = [
    path("<int:project_id>/time_tracking/",views.time_tracking_overview,name="overview"),
    path("<int:project_id>/time_tracking/<int:entry_id>/edit/",views.time_tracking_edit,name="edit"),
    path("<int:project_id>/time_tracking/<int:entry_id>/delete/",views.time_tracking_delete,name="delete"),
]