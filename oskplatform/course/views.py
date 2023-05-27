from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from password_generator import PasswordGenerator
from users.models import CustomUser, Student
from course.models import PracticalLesson, Course
from django.utils import timezone
from course.forms import NewStudentForm

@login_required(login_url='/login')
def panel_view(request):
    template = loader.get_template('panel.html')
    return HttpResponse(template.render({}, request))

@login_required(login_url='/login')
def upcoming_lessons_view(request):
    user_courses = Course.objects.filter(student=request.user.student, course_status='R')
    all_practical_lessons = []
    for course in user_courses:
        practical_lessons = PracticalLesson.objects.filter(course=course, date__gte=timezone.now())
        for lesson in practical_lessons:
            all_practical_lessons.append(lesson)
    all_practical_lessons.sort(key=lambda x: x.date)
    template = loader.get_template('upcoming_lessons.html')
    context = {
        'lessons': all_practical_lessons
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def register_student_view(request):
    if request.user.permissions_type != 'E':
        return HttpResponse('Nie masz uprawnień do tej strony')
    if request.method == 'POST':
        form = NewStudentForm(request.POST)
        if form.is_valid():
            surname = request.POST.get('surname')
            name = request.POST.get('name')
            birth_date = request.POST.get('birth_date')
            phone_number = request.POST.get('phone_number')
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
        else:
            return HttpResponse('Niepoprawne dane')
        return HttpResponse(f'Utworzono nowego kursanta {student} o nazwie użytkownika {user.username} i haśle {password}')
    template = loader.get_template('register_student.html')
    return HttpResponse(template.render({}, request))
