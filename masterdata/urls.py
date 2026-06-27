from django.urls import path
from . import views


app_name = "masterdata"

urlpatterns = [
    path("",views.overview,name="overview"),
    path("<str:model_name>/",views.setting_detail,name="detail"),
    path("<str:model_name>/add/",views.setting_add,name="add"),
    path("<str:model_name>/<int:pk>/delete/",views.setting_delete,name="delete"),
    path("update/check/", views.update_check, name="update_check"),
    path("update/apply/",  views.update_apply,  name="update_apply"),
]