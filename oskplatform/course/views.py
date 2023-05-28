from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from password_generator import PasswordGenerator
from users.models import CustomUser, Student, Employee, Instructor, Qualification
from course.models import PracticalLesson, Course, Category, Vehicle
from django.utils import timezone
from course.forms import NewStudentForm, SetPasswordForm, EditPracticalLessonForm, CreatePracticalLessonForm
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
        messages.error(request, 'Nie ma takiego kursu')
        return redirect('/courses')
    course = Course.objects.get(pk=course_id)
    if request.user.permissions_type == "S" and course.student != request.user.student:
        messages.error(request, 'Nie ma takiego kursu')
        return redirect('/courses')
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
        messages.error(request, 'Nie ma takiej jazdy')
        return redirect('/upcoming_lessons')
    lesson = PracticalLesson.objects.get(pk=practical_id)
    if request.user.permissions_type == "S" and lesson.course.student != request.user.student:
        messages.error(request, 'Nie ma takiej jazdy')
        return redirect('/upcoming_lessons')
    context = {
        'lesson': lesson
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def change_practical_lesson_status_view(request, practical_id):
    if request.user.permissions_type == "S":
        messages.error(request, 'Nie masz uprawnień do tej strony')
        return redirect(f'/practical/{practical_id}')
    if not PracticalLesson.objects.filter(pk=practical_id).exists():
        messages.error(request, 'Nie ma takiej jazdy')
        return redirect('/upcoming_lessons')
    lesson = PracticalLesson.objects.get(pk=practical_id)
    if request.user.permissions_type == "I" and lesson.instructor != request.user.instructor:
        messages.error(request, 'Nie posiadasz wymaganych uprawnień')
        return redirect(f'/practical/{practical_id}')
    if lesson.is_cancelled:
        lesson.is_cancelled = False
    else:
        lesson.is_cancelled = True
    lesson.save()
    return redirect(f'/practical/{practical_id}')

@login_required(login_url='/login')
def edit_practical_lesson_view(request, practical_id):
    
    if request.user.permissions_type == "S":
        messages.error(request, 'Nie masz uprawnień do tej strony')
        return redirect('/upcoming_lessons')
    if not PracticalLesson.objects.filter(pk=practical_id).exists():
        messages.error(request, 'Nie ma takiej lekcji')
        return redirect('/upcoming_lessons')
    lesson = PracticalLesson.objects.get(pk=practical_id)
    if request.user.permissions_type == "I" and lesson.instructor != request.user.instructor:
        messages.error(request, 'Nie posiadasz wymaganych uprawnień')
        return redirect(f'/practical/{practical_id}')
    
    if request.method == 'POST':
        form = EditPracticalLessonForm(request.POST)
        if form.is_valid():
            lesson.cost = form.cleaned_data['cost']
            lesson.date = form.cleaned_data['date']
            lesson.start_time = form.cleaned_data['start_time']
            lesson.num_of_hours = form.cleaned_data['num_of_hours']
            lesson.num_of_km = form.cleaned_data['num_of_km']
            lesson.vehicle = form.cleaned_data['vehicle']
            if request.user.permissions_type != "I":
                lesson.instructor = form.cleaned_data['instructor']
            lesson.save()
            return redirect(f'/practical/{practical_id}')
        else:
            messages.error(request, 'Wprowadzono niepoprawne dane')

    template = loader.get_template('practical_edit.html')
    vehicles = [None]
    for vehicle in Vehicle.objects.filter(is_available=True):
        vehicles.append(vehicle)
        
    if lesson.vehicle is not None:
        vehicles.remove(lesson.vehicle)
        vehicles.insert(0, lesson.vehicle)
        
    instructors = []
    for instructor in Instructor.objects.filter(is_active=True):
        instructors.append(instructor)
    if lesson.instructor  in instructors:
        instructors.remove(lesson.instructor)
    instructors.insert(0, lesson.instructor)
    
    context = {
        'lesson': lesson,
        'vehicles': vehicles,
        'instructors': instructors
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def delete_practical_lesson_view(request, practical_id):
    if request.user.permissions_type == "S":
        messages.error(request, 'Nie masz uprawnień do tej strony')
        return redirect('/upcoming_lessons')
    if not PracticalLesson.objects.filter(pk=practical_id).exists():
        messages.error(request, 'Nie ma takiej jazdy')
        return redirect('/upcoming_lessons')
    lesson = PracticalLesson.objects.get(pk=practical_id)
    if request.user.permissions_type == "I" and lesson.instructor != request.user.instructor:
        messages.error(request, 'Nie posiadasz wymaganych uprawnień')
        return redirect(f'/practical/{practical_id}')
    if lesson.date < timezone.now().date():
        messages.error(request, 'Nie można usunąć jazdy, która już się odbyła')
        return redirect(f'/practical/{practical_id}')
    lesson.delete()
    return redirect('/upcoming_lessons')

@login_required(login_url='/login')
def create_practical_lesson_view(request, course_id=None):
    
    template = loader.get_template('practical_create.html')
    
    instructor_qualifications = []
    for qualification in Qualification.objects.filter(instructor=request.user.instructor):
        instructor_qualifications.append(qualification.category)
            
    if request.user.permissions_type != "I":
        messages.error(request, 'Nie masz uprawnień do tej strony')
        return redirect('/upcoming_lessons')
    
    if course_id != None:
        if not Course.objects.filter(pk=course_id).exists():
            messages.error(request, 'Nie ma takiego kursu')
            return redirect('/courses')
        selected_course = Course.objects.get(pk=course_id)
        if selected_course.course_status != 'R':
            messages.error(request, 'Nie można dodać jazdy do zakończonego kursu')
            return redirect('/courses')
        if selected_course.category not in instructor_qualifications:
            messages.error(request, 'Nie posiadasz wymaganych uprawnień')
            return redirect('/courses')
    
    courses = []
    for course in Course.objects.filter(course_status='R', category__symbol__in=instructor_qualifications):
        courses.append(course)
    if course_id != None:
        courses.remove(selected_course)
        courses.insert(0, selected_course)
        
    vehicles = [None]
    for vehicle in Vehicle.objects.filter(is_available=True).exclude(type__contains='P'):
        vehicles.append(vehicle)
        
    if request.method == 'POST':
        form = CreatePracticalLessonForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['course'] not in courses:
                messages.error(request, 'Nie ma takiego kursu')
                return redirect('/courses')
            PracticalLesson.objects.create(
                course=form.cleaned_data['course'],
                date=form.cleaned_data['date'],
                start_time=form.cleaned_data['start_time'],
                num_of_hours=form.cleaned_data['num_of_hours'],
                num_of_km=form.cleaned_data['num_of_km'],
                cost=form.cleaned_data['cost'],
                instructor=request.user.instructor,
                vehicle=form.cleaned_data['vehicle']
            )
            messages.success(request, 'Dodano nową jazdę')
            return redirect('/upcoming_lessons')
        else:
            messages.error(request, 'Wprowadzono niepoprawne dane')
            
    context = {
        'instructor': request.user.instructor,
        'vehicles': vehicles,
        'courses': courses
    }
    
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def register_student_view(request):
    template = loader.get_template('register_student.html')
    if request.user.permissions_type not in {'A', 'E'} :
        messages.error(request, 'Nie masz uprawnień do tej strony')
        return redirect('/upcoming_lessons')
    if request.method == 'POST':
        form = NewStudentForm(request.POST)
        if form.is_valid():
            surname = request.POST.get('surname')
            name = request.POST.get('name')
            birth_date = request.POST.get('birth_date')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')
            next_user_id = CustomUser.objects.order_by('-pk')[0].pk + 1
            username = f'{surname.lower()[:3]}{name.lower()[:3]}{next_user_id}'
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
            messages.error(request, 'Wprowadzono niepoprawne dane')
            return HttpResponse(template.render({}, request))
        return HttpResponse(f'Utworzono nowego kursanta {student} o nazwie użytkownika {user.username} i haśle {password}')
    return HttpResponse(template.render({}, request))
