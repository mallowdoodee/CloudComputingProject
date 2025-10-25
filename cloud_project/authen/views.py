# authen/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from authen.forms import RegistrationForm


class LoginView(View):
    def get(self, request):
        authen_form = AuthenticationForm()
        return render(request, 'login.html', {"form": authen_form})
    
    def post(self, request):
        authen_form = AuthenticationForm(data=request.POST)
        if authen_form.is_valid():
            user = authen_form.get_user()
            login(request, user)
            return redirect('appointment-list')

        messages.error(request, "Invalid username or password.")
        return render(request, 'login.html', {"form": authen_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('login')

def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Registration successful! Welcome, {user.username}")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})
