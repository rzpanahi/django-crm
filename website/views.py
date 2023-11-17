from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def home(request):
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
        return render(request, "home.html", {})


def logout_user(request):
    pass
