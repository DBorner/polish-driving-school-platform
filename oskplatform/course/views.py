from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from password_generator import PasswordGenerator
from users.models import CustomUser, Student, Employee, Instructor
from course.models import PracticalLesson, Course, Category
from django.utils import timezone
from course.forms import NewStudentForm, SetPasswordForm
from django.contrib import messages
from django.shortcuts import redirect

@login_required(login_url='/login')
def panel_view(request):
    if request.user.permissions_type in {'S', 'I'}:
        return redirect('/upcoming_lessons')
    template = loader.get_template('panel.html')
    return HttpResponse(template.render({}, request))

@login_required(login_url='/login')
def profile_settings_view(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Poprawnie zmieniłeś hasło")
            return redirect('/login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    if user.permissions_type == 'S':
        user_info = user.student
    elif user.permissions_type == 'I':
        user_info = user.instructor
    else:
        user_info = user.employee
    template = loader.get_template('profile_settings.html')
    context = {'user_info': user_info}
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def upcoming_lessons_view(request):
    all_practical_lessons = []
    if request.user.permissions_type == 'S':
        user_courses = Course.objects.filter(student=request.user.student, course_status='R')
        for course in user_courses:
            practical_lessons = PracticalLesson.objects.filter(course=course, date__gte=timezone.now())
            for lesson in practical_lessons:
                all_practical_lessons.append(lesson)
        all_practical_lessons.sort(key=lambda x: x.date)
    elif request.user.permissions_type == 'I':
        all_practical_lessons = PracticalLesson.objects.filter(instructor=request.user.instructor, date__gte=timezone.now())
        all_practical_lessons = all_practical_lessons.order_by('date')
    else:
        all_practical_lessons = PracticalLesson.objects.filter(date__gte=timezone.now())
        all_practical_lessons = all_practical_lessons.order_by('date')
    template = loader.get_template('upcoming_lessons.html')
    context = {
        'lessons': all_practical_lessons
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def courses_view(request):
    if request.user.permissions_type == 'S':
        user_courses = Course.objects.filter(student=request.user.student)
    elif request.user.permissions_type == 'I':
        user_courses = Course.objects.filter(instructor=request.user.instructor, course_status='R')
    else:
        user_courses = Course.objects.all()
    data = []
    for course in user_courses:
        practical_lessons = PracticalLesson.objects.filter(course=course, date__lt=timezone.now(), is_cancelled=False)
        practical_hours = 0
        for lesson in practical_lessons:
            practical_hours += lesson.num_of_hours
        done_percentage = practical_hours/course.category.required_practical_hours*100
        if done_percentage > 100:
            done_percentage = 100
        data.append({
            'course': course,
            'done_percentage': done_percentage
        })
    template = loader.get_template('courses.html')
    context = {
        'courses': data
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def course_detail_view(request, course_id):
    template = loader.get_template('course_detail.html')
    if not Course.objects.filter(pk=course_id).exists():
        return HttpResponse('Nie ma takiego kursu')
    course = Course.objects.get(pk=course_id)
    if request.user.permissions_type == "S" and course.student != request.user.student:
        return HttpResponse('Nie ma takiego kursu')
    lessons = PracticalLesson.objects.filter(course=course)
    lessons = lessons.order_by('date')
    context = {
        'course': course,
        'lessons': lessons
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def practical_detail_view(request, practical_id):
    template = loader.get_template('practical_detail.html')
    if not PracticalLesson.objects.filter(pk=practical_id).exists():
        return HttpResponse('Nie ma takiej lekcji')
    lesson = PracticalLesson.objects.get(pk=practical_id)
    if request.user.permissions_type == "S" and lesson.course.student != request.user.student:
        return HttpResponse('Nie ma takiej lekcji')
    context = {
        'lesson': lesson
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
