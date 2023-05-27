from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def user_info(request):
    return HttpResponse("User Info Page")


def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"Zalogowałeś się jako {username}.")
				return redirect("/")
			else:
				messages.error(request,"Niepoprawna nazwa użytkownika lub hasło.")
		else:
			messages.error(request,"Niepoprawna nazwa użytkownika lub hasło.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})


def logout_view(request):
	logout(request)
	messages.info(request, "Wylogowałeś się.") 
	return redirect("/")