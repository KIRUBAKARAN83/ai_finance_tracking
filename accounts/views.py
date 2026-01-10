from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

app_name = "accounts"
def register(request):
    """
    User registration (signup)
    Creates a new user and logs them in immediately
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after signup
            return redirect("/")  # dashboard
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    """
    Optional profile page (future use)
    """
    return render(request, "profile.html")
