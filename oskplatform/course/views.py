from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from password_generator import PasswordGenerator

from users.models import CustomUserMenager, CustomUser, Student

@login_required(login_url='/login')
def panel_view(request):
    template = loader.get_template('panel.html')
    return HttpResponse(template.render({}, request))

@login_required(login_url='/login')
def register_student_view(request):
    if request.user.permissions_type != 'E':
        return HttpResponse('Nie masz uprawnień do tej strony')
    if request.method == 'POST':
        surname = request.POST.get('surname')
        name = request.POST.get('name')
        birth_date = request.POST.get('birth-date')
        phone_number = request.POST.get('phone-number')
        email = request.POST.get('email')
        id = CustomUser.objects.order_by('-pk')[0].pk + 1
        username = f'{surname.lower()[:3]}{name.lower()[:3]}{id}'
        pwo = PasswordGenerator()
        pwo.minlen = 6
        pwo.maxlen = 6
        password = pwo.generate()
        print(password)
        student = Student.objects.create(surname=surname, name=name, birth_date=birth_date, phone_number=phone_number, email=email)
        user = CustomUser.objects.create_user(username=username, password=password, permissions_type='S', student=student)
        student.save()
        user.save()
        return HttpResponse(f'Utworzono nowego kursanta {student} o nazwie użytkownika {user.username} i haśle {password}')
    template = loader.get_template('register_student.html')
    return HttpResponse(template.render({}, request))
