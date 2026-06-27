from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("", views.overview, name="overview"),

    path("add/",views.user_add,name="user_add"),
    path("<int:user_id>/edit/",views.user_edit,name="user_edit"),
    path("<int:user_id>/archive/",views.user_archive,name="user_archive"),
    path("<int:user_id>/reactivate/",views.user_reactivate,name="user_reactivate"),
    
    path("role/add/",views.role_add,name="role_add"),
    path("role/<int:role_id>/edit/",views.role_edit,name="role_edit"),
    path("role/<int:role_id>/delete/",views.role_delete,name="role_delete"),
]