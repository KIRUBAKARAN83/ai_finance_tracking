from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, profile  # keep your custom views
app_name = "accounts"   # <-- add this for namespacing

urlpatterns = [
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),

    # Login and logout using Django built-in views
   
]

