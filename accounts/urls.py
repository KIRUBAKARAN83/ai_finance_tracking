# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, profile

urlpatterns = [
    # Registration
    path("register/", register, name="register"),

    # Profile
    path("profile/", profile, name="profile"),

    # Login / Logout (using Django’s built-in views)
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
