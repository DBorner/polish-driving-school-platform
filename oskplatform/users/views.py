from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views import View


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "login.html", {"login_form": form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Zalogowałeś się jako {username}.")
                return redirect("/")
            else:
                messages.error(request, "Niepoprawna nazwa użytkownika lub hasło.")
        else:
            messages.error(request, "Niepoprawna nazwa użytkownika lub hasło.")
        return render(request, "login.html", {"login_form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Wylogowałeś się.")
    return redirect("/")
