from django.contrib.messages.api import success
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import AddRecordForm, RegisterForm
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
        return render(request, "home.html", {"records": records})


def logout_user(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect("home")
    else:
        messages.success(request, "Error with logging out")


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
            return redirect("home")
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})

    return render(request, "register.html", {"form": form})


def customer_record(request, pk):
    if not request.user.is_authenticated:
        messages.success(request, "You must be logged in")
        return redirect("home")

    customer_record = Record.objects.get(id=pk)

    if not customer_record:
        messages.success(request, "No record found!")
        return render(request, "record.html", {})

    return render(request, "record.html", {"customer_record": customer_record})


def delete_record(request, pk):
    if not request.user.is_authenticated:
        messages.success(request, "You must be logged in")
        return render(request, "home.html", {})

    record = Record.objects.get(id=pk)
    record.delete()

    messages.success(
        request, f"{record.first_name} {record.last_name} deleted successfully!"
    )
    return redirect("home")


def add_record(request):
    if not request.user.is_authenticated:
        messages.success(request, "You must be logged in")
        return render(request, "home.html", {})

    if request.method == "GET":
        form = AddRecordForm()
        return render(request, "add.html", {"form": form})

    form = AddRecordForm(request.POST)

    if not form.is_valid():
        return render(request, "add.html", {"form": form})

    record = form.save()
    messages.success(
        request,
        f"{record.first_name} {record.last_name} added successfully!",
    )
    return redirect("home")


# def update_record(request, pk):
#     if request.user.is_authenticated:
#         current_record = Record.objects.get(id=pk)
#         form = AddRecordForm(request.POST or None, instance=current_record)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Record Has Been Updated!")
#             return redirect("home")
#         return render(request, "record.html", {"form": form})
#     else:
#         messages.success(request, "You Must Be Logged In...")
#         return redirect("home")


def update_record(request, pk):
    if not request.user.is_authenticated:
        messages.success(request, "You must be logged in")
        return render(request, "home.html", {})

    current_record = Record.objects.get(id=pk)

    if request.method == "GET":
        form = AddRecordForm(instance=current_record)
        return render(request, "update.html", {"form": form})

    form = AddRecordForm(request.POST)

    if not form.is_valid():
        return render(request, "update.html", {"form": form})

    if form.is_valid():
        form.save()
        messages.success(request, "Record successfully Updated!")
        return redirect("home")
