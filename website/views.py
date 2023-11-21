from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm
from .models import Record 

def home(request):
    records = Record.objects.all()

    if request.method == "POST":
        # user is not logged in
        username = request.POST["username"]
        password = request.POST["password"]

        # authenticatet
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
        else:
            messages.success(request, "username or password incorrect")

        return redirect("home")

    elif request.method == "GET":
        # user is logged in
        return render(request, "home.html", { 'records': records})


def logout_user(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect("home")
    else:
        messages.success("Error with logging out")


def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            # authecticate and login
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            first_name = form.cleaned_data["first_name"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, f"Welcome {first_name}, you have logged in :)")
            return redirect('home')
    else:
        form = RegisterForm()
        return render(request, "register.html", { 'form': form })

    return render(request, "register.html", { 'form': form })