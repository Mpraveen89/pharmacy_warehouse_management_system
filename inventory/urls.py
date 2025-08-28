from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),

    path("medicines/", views.medicine_list, name="medicine_list"),
    path("medicines/new/", views.medicine_create, name="medicine_create"),
    path("medicines/<int:pk>/", views.medicine_detail, name="medicine_detail"),

    path("batches/", views.batch_list, name="batch_list"),
    path("batches/new/", views.batch_create, name="batch_create"),
    path("batches/<int:pk>/", views.batch_detail, name="batch_detail"),

    path("moves/", views.movement_list, name="movement_list"),
    path("moves/new/", views.movement_create, name="movement_create"),

    path("addresses/", views.address_list, name="address_list"),
    path("addresses/new/", views.address_create, name="address_create"),
]
