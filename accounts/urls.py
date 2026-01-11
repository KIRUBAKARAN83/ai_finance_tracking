

# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, profile

app_name = "accounts"

urlpatterns = [
    # Custom views
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),

    # Built-in authentication views
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="accounts:login"),
        name="logout",
    ),
]

