from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, profile  # keep your custom views
app_name = "accounts"   # <-- add this for namespacing

urlpatterns = [
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),

    # Login and logout using Django built-in views
   ]

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, profile

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),

    # Login and logout using Django built-in views
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="templates/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="accounts:login"),
        name="logout",
    ),

]
