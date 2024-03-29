from django.http import HttpResponse
from django.template import loader
from users.models import CustomUser, Student, Instructor, Qualification, Employee
from course.models import PracticalLesson, Course, Category, Vehicle, TheoryCourse
from django.utils import timezone
from course.forms import (
    NewStudentForm,
    EditPracticalLessonForm,
    CreatePracticalLessonForm,
    CreateCourseForm,
    EditCourseForm,
    EditStudentForm,
    NewTheoryForm,
    TheoryEditForm,
    VehicleForm,
    CreateCategoryForm,
    EditCategoryForm,
    CreateQualificationForm,
    NewPasswordForm,
    InstructorForm,
    EmployeeForm,
)
from datetime import datetime, date
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from course.utils import (
    check_instructor_qualifications,
    is_student_active,
    requires_permissions,
    generate_password,
    check_start_date_for_theory_course,
)
from django.db.models import Q
from django.views import View
from django.utils.decorators import method_decorator
from datetime import datetime, date

class ProfileSettingsView(View):
    template = loader.get_template("profile_settings.html")

    @method_decorator(
        requires_permissions(
            permission_type=["S", "I", "E", "A"],
            redirect_url="/login",
            redirect_message="Musisz być zalogowanym",
        )
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.permissions_type == "S":
            user_info = user.student
        elif user.permissions_type == "I":
            user_info = user.instructor
        else:
            user_info = user.employee
        context = {"user_info": user_info}
        return HttpResponse(self.template.render(context, request))

    @method_decorator(
        requires_permissions(
            permission_type=["S", "I", "E", "A"],
            redirect_url="/login",
            redirect_message="Musisz być zalogowanym",
        )
    )
    def post(self, request):
        user = request.user
        form = NewPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hasło zostało zmienione")
            return redirect("/profile_settings")
        else:
            messages.error(request, "Podano nieprawidłowe hasło")
            return redirect("/profile_settings")


class UpcomingLessonsView(View):
    template = loader.get_template("upcoming_lessons.html")

    @method_decorator(requires_permissions(permission_type=["S", "I", "E", "A"]))
    def get(self, request, *args, **kwargs):
        all_practical_lessons = []
        if request.user.permissions_type == "S":
            all_practical_lessons = self._get_student_lessons(request.user.student)

        elif request.user.permissions_type == "I":
            all_practical_lessons = PracticalLesson.objects.filter(
                instructor=request.user.instructor, date__gte=timezone.now()
            )
            all_practical_lessons = all_practical_lessons.order_by("date", "start_time")
        else:
            all_practical_lessons = PracticalLesson.objects.filter(
                date__gte=timezone.now()
            )
            all_practical_lessons = all_practical_lessons.order_by("date", "start_time")

        context = {"lessons": all_practical_lessons}
        return HttpResponse(self.template.render(context, request))

    def _get_student_lessons(self, student):
        lessons = []
        user_courses = Course.objects.filter(student=student, course_status="R")
        for course in user_courses:
            practical_lessons = PracticalLesson.objects.filter(
                course=course, date__gte=timezone.now()
            )
            for lesson in practical_lessons:
                lessons.append(lesson)
        lessons.sort(key=lambda x: x.date)
        return lessons


class CoursesView(View):
    template = loader.get_template("courses.html")

    @method_decorator(requires_permissions(permission_type=["S", "I", "E", "A"]))
    def get(self, request, student_id=None, *args, **kwargs):
        if request.user.permissions_type == "S":
            user_courses = Course.objects.filter(student=request.user.student)
        elif request.user.permissions_type == "I":
            user_courses = Course.objects.filter(
                instructor=request.user.instructor, course_status="R"
            )
        else:
            if student_id:
                user_courses = Course.objects.filter(student_id=student_id)
            else:
                user_courses = Course.objects.all()
            user_courses = user_courses.order_by("course_status", "-start_date")
        data = []
        for course in user_courses:
            data.append(
                {
                    "course": course,
                    "done_percentage": self._calculate_done_percentage(course),
                }
            )
        context = {"courses": data}
        return HttpResponse(self.template.render(context, request))

    def _calculate_done_percentage(self, course):
        practical_lessons = PracticalLesson.objects.filter(
            course=course, date__lt=timezone.now(), is_cancelled=False
        )
        practical_hours = 0
        for lesson in practical_lessons:
            practical_hours += lesson.num_of_hours
        done_percentage = (
            practical_hours / course.category.required_practical_hours * 100
        )
        if done_percentage > 100:
            done_percentage = 100
        return done_percentage


class CourseDetailView(View):
    template = loader.get_template("course_detail.html")

    @method_decorator(requires_permissions(permission_type=["S", "I", "E", "A"]))
    def get(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, pk=course_id)

        if (
            request.user.permissions_type == "S"
            and course.student != request.user.student
        ):
            messages.error(request, "Nie ma takiego kursu")
            return redirect("/courses")

        lessons = PracticalLesson.objects.filter(course=course)
        lessons = lessons.order_by("-date", "start_time")
        context = {"course": course, "lessons": lessons}
        return HttpResponse(self.template.render(context, request))


class PracticalDetailView(View):
    template = loader.get_template("practical_detail.html")

    @method_decorator(requires_permissions(permission_type=["S", "I", "E", "A"]))
    def get(self, request, practical_id, *args, **kwargs):
        lesson = get_object_or_404(PracticalLesson, pk=practical_id)

        if (
            request.user.permissions_type == "S"
            and lesson.course.student != request.user.student
        ):
            messages.error(request, "Nie ma takiej jazdy")
            return redirect("/upcoming_lessons")

        context = {"lesson": lesson}
        return HttpResponse(self.template.render(context, request))


@requires_permissions(permission_type=["I", "E", "A"])
def change_practical_lesson_status_view(request, practical_id):
    lesson = get_object_or_404(PracticalLesson, pk=practical_id)
    if (
        request.user.permissions_type == "I"
        and lesson.instructor != request.user.instructor
    ):
        messages.error(request, "Nie posiadasz wymaganych uprawnień")
        return redirect(f"/practical/{practical_id}")
    if lesson.is_cancelled:
        if PracticalLesson.objects.filter(
            instructor=lesson.instructor, date=lesson.date, start_time=lesson.start_time, is_cancelled=False).exists():
            messages.error(request, "Nie można zapisać dwóch jazd w tym samym czasie")
            return redirect(f"/practical/{practical_id}")
        lesson.is_cancelled = False
    else:
        lesson.is_cancelled = True
    lesson.save()
    return redirect(f"/practical/{practical_id}")


@requires_permissions(permission_type=["I", "E", "A"])
def delete_practical_lesson_view(request, practical_id):
    lesson = get_object_or_404(PracticalLesson, pk=practical_id)
    if (
        request.user.permissions_type == "I"
        and lesson.instructor != request.user.instructor
    ):
        messages.error(request, "Nie posiadasz wymaganych uprawnień")
        return redirect(f"/practical/{practical_id}")
    if lesson.date < timezone.now().date():
        messages.error(request, "Nie można usunąć jazdy, która już się odbyła")
        return redirect(f"/practical/{practical_id}")
    lesson.delete()
    return redirect("/upcoming_lessons")


class EditPracticalLessonView(View):
    template = loader.get_template("practical_edit.html")

    def _check_instructor_permissions(self, request, lesson):
        if (
            request.user.permissions_type == "I"
            and lesson.instructor != request.user.instructor
        ):
            messages.error(request, "Nie posiadasz wymaganych uprawnień")
            return False
        return True

    @method_decorator(requires_permissions(permission_type=["I", "E", "A"]))
    def get(self, request, practical_id, *args, **kwargs):
        lesson = get_object_or_404(PracticalLesson, pk=practical_id)
        if self._check_instructor_permissions(request, lesson) == False:
            return redirect(f"/practical/{practical_id}")
        template = loader.get_template("practical_edit.html")
        vehicles = [None]
        for vehicle in Vehicle.objects.filter(is_available=True):
            vehicles.append(vehicle)

        if lesson.vehicle is not None:
            vehicles.remove(lesson.vehicle)
            vehicles.insert(0, lesson.vehicle)

        instructors = []
        for instructor in Instructor.objects.filter(is_active=True):
            instructors.append(instructor)
        if lesson.instructor in instructors:
            instructors.remove(lesson.instructor)
        instructors.insert(0, lesson.instructor)

        context = {"lesson": lesson, "vehicles": vehicles, "instructors": instructors}
        return HttpResponse(template.render(context, request))

    @method_decorator(requires_permissions(permission_type=["I", "E", "A"]))
    def post(self, request, practical_id, *args, **kwargs):
        lesson = get_object_or_404(PracticalLesson, pk=practical_id)
        if self._check_instructor_permissions(request, lesson) == False:
            return redirect(f"/practical/{practical_id}")
        form = EditPracticalLessonForm(request.POST)
        if form.is_valid():
            if PracticalLesson.objects.filter(
                instructor=request.user.instructor,
                date=form.cleaned_data["date"],
                start_time=form.cleaned_data["start_time"],
                is_cancelled=False,
            ).exists() and lesson != PracticalLesson.objects.filter(
                instructor=request.user.instructor,
                date=form.cleaned_data["date"],
                start_time=form.cleaned_data["start_time"],
                is_cancelled=False,
            ).first():
                messages.error(
                    request, "Nie można zapisać dwóch jazd w tym samym czasie"
                )
                return redirect(f"/practical/{practical_id}/edit")
            lesson.cost = form.cleaned_data["cost"]
            lesson.date = form.cleaned_data["date"]
            lesson.start_time = form.cleaned_data["start_time"]
            lesson.num_of_hours = form.cleaned_data["num_of_hours"]
            lesson.num_of_km = form.cleaned_data["num_of_km"]
            lesson.vehicle = form.cleaned_data["vehicle"]
            if request.user.permissions_type != "I":
                if request.POST.get("instructor") != "" and Instructor.objects.filter(pk=request.POST.get("instructor")).exists():
                    lesson.instructor = Instructor.objects.get(pk=request.POST.get("instructor"))
            lesson.save()
            return redirect(f"/practical/{practical_id}")
        else:
            messages.error(request, "Wprowadzono niepoprawne dane")
            return redirect(f"/practical/{practical_id}/edit")


class CreatePracticalLessonView(View):
    template = loader.get_template("practical_create.html")

    @method_decorator(requires_permissions(permission_type=["I"]))
    def get(self, request, course_id=None, *args, **kwargs):
        instructor_qualifications = []
        for qualification in Qualification.objects.filter(
            instructor=request.user.instructor
        ):
            instructor_qualifications.append(qualification.category)

        if course_id != None:
            selected_course = get_object_or_404(Course, pk=course_id)
            if selected_course.course_status != "R":
                messages.error(request, "Nie można dodać jazdy do zakończonego kursu")
                return redirect("/courses")
            if selected_course.category not in instructor_qualifications:
                messages.error(request, "Nie posiadasz wymaganych uprawnień")
                return redirect("/courses")

        courses = []
        for course in Course.objects.filter(
            course_status="R", category__symbol__in=instructor_qualifications
        ):
            courses.append(course)
        if course_id != None:
            courses.remove(selected_course)
            courses.insert(0, selected_course)

        vehicles = [None]
        for vehicle in Vehicle.objects.filter(is_available=True).exclude(
            type__contains="P"
        ):
            vehicles.append(vehicle)

        context = {
            "instructor": request.user.instructor,
            "vehicles": vehicles,
            "courses": courses,
        }

        return HttpResponse(self.template.render(context, request))

    @method_decorator(requires_permissions(permission_type=["I"]))
    def post(self, request, course_id=None, *args, **kwargs):
        form = CreatePracticalLessonForm(request.POST)
        if form.is_valid():
            instructor_qualifications = []
            for qualification in Qualification.objects.filter(
                instructor=request.user.instructor
            ):
                instructor_qualifications.append(qualification.category)
            courses = Course.objects.filter(
                course_status="R", category__symbol__in=instructor_qualifications
            )

            if form.cleaned_data["course"] not in courses:
                messages.error(request, "Nie ma takiego kursu")
                return redirect("/practical/create")
            if form.cleaned_data["date"] < timezone.now().date():
                messages.error(request, "Nie można dodać jazdy, która już się odbyła")
                return redirect("/practical/create")
            if PracticalLesson.objects.filter(
                instructor=request.user.instructor,
                date=form.cleaned_data["date"],
                start_time=form.cleaned_data["start_time"],
                is_cancelled=False,
            ).exists():
                messages.error(
                    request, "Nie można zapisać dwóch jazd w tym samym czasie"
                )
                return redirect("/practical/create")
            practical_lesson = form.save(commit=False)
            practical_lesson.instructor = request.user.instructor
            practical_lesson.save()
            messages.success(request, "Dodano nową jazdę")
            return redirect("/upcoming_lessons")
        else:
            messages.error(request, "Wprowadzono niepoprawne dane")
            return redirect("/practical/create")


class CreateCourseView(View):
    template = loader.get_template("course_create.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request, student_id=None):
        if student_id != None:
            selected_student = get_object_or_404(Student, pk=student_id)

        categories = Category.objects.filter(is_available=True)

        instructors = [None]
        for instructor in Instructor.objects.filter(is_active=True):
            instructors.append(instructor)

        students = []
        for student in Student.objects.all():
            students.append(student)
        if student_id != None:
            students.remove(selected_student)
            students.insert(0, selected_student)

        context = {
            "instructors": instructors,
            "students": students,
            "categories": categories,
        }
        return HttpResponse(self.template.render(context, request))

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def post(self, request, student_id=None):
        form = CreateCourseForm(request.POST)
        if form.is_valid() and check_instructor_qualifications(
            form.cleaned_data["instructor"], form.cleaned_data["category"]
        ):
            if len(form.cleaned_data['pkk_number']) != 20:
                messages.error(request, "Numer PKK musi mieć 20 cyfr")
                return redirect("/courses/create")
            Course.objects.create(
                pkk_number=form.cleaned_data["pkk_number"],
                cost=form.cleaned_data["cost"],
                category=form.cleaned_data["category"],
                student=form.cleaned_data["student"],
                instructor=form.cleaned_data["instructor"],
                course_status="R",
                start_date=timezone.now(),
            )
            messages.success(request, "Dodano nowy kurs")
            return redirect("/courses")
        else:
            messages.error(request, f"Wprowadzono niepoprawne dane: {form.errors}")
            if student_id:
                return redirect(f"/courses/create/{student_id}")
            else:
                return redirect("/courses/create")


class EditCourseView(View):
    template = loader.get_template("course_edit.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        instructors = []
        for instructor in Instructor.objects.filter(is_active=True):
            instructors.append(instructor)
        if course.instructor != None:
            instructors.remove(course.instructor)
            instructors.insert(0, course.instructor)
        else:
            instructors.insert(0, None)
        context = {"course": course, "instructors": instructors}
        return HttpResponse(self.template.render(context, request))

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def post(self, request, course_id):
        form = EditCourseForm(request.POST)
        if form.is_valid() and check_instructor_qualifications(
            form.cleaned_data["instructor"], Course.objects.get(pk=course_id).category
        ):
            course = Course.objects.get(pk=course_id)
            course.instructor = form.cleaned_data["instructor"]
            course.course_status = form.cleaned_data["course_status"]
            course.save()
            messages.success(request, "Zmieniono dane kursu")
            return redirect(f"/courses/{course_id}")
        else:
            messages.error(request, f"Wprowadzono niepoprawne dane {form.errors}")
            return redirect(f"/courses/{course_id}/edit")


class StudentsView(View):
    template = loader.get_template("students.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request):
        if request.GET.get("q") != None:
            students = self._search_results(request)
        else:
            students = Student.objects.all().order_by("-id")
        context = {"students": students}
        return HttpResponse(self.template.render(context, request))

    def _search_results(self, request):
        query = request.GET.get("q")
        students = Student.objects.filter(
            Q(name__icontains=query) | Q(surname__icontains=query)
        )
        if request.GET.get("status") == "active":
            temp_students = []
            for student in students:
                if is_student_active(student):
                    temp_students.append(student)
            return temp_students
        elif request.GET.get("status") == "inactive":
            temp_students = []
            for student in students:
                if not is_student_active(student):
                    temp_students.append(student)
            return temp_students
        return students


class RegisterStudentView(View):
    template = loader.get_template("register_student.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request):
        return HttpResponse(self.template.render({}, request))

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def post(self, request):
        form = NewStudentForm(request.POST)
        if form.is_valid():
            surname = request.POST.get("surname")
            name = request.POST.get("name")
            birth_date = request.POST.get("birth_date")
            phone_number = request.POST.get("phone_number")
            email = request.POST.get("email")
            next_user_id = CustomUser.objects.order_by("-pk")[0].pk + 1
            username = f"{surname.lower()[:3]}{name.lower()[:3]}{next_user_id}"
            password = generate_password()
            student = Student.objects.create(
                surname=surname,
                name=name,
                birth_date=birth_date,
                phone_number=phone_number,
                email=email,
            )
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                permissions_type="S",
                student=student,
            )
            student.save()
            user.save()
        else:
            messages.error(request, "Wprowadzono niepoprawne dane")
            return HttpResponse(self.template.render({}, request))
        messages.success(
            request,
            f"""Dodano nowego kursanta - dane logowania:
                         Login: {username}
                         Hasło: {password}""",
        )
        return redirect("/students")


@requires_permissions(permission_type=["E", "A"])
def create_account_for_student_view(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if CustomUser.objects.filter(student=student).exists():
        messages.error(request, "Konto dla tego kursanta już istnieje")
        return redirect(f"/students/{student_id}")
    next_user_id = CustomUser.objects.order_by("-pk")[0].pk + 1
    username = f"{student.surname.lower()[:3]}{student.name.lower()[:3]}{next_user_id}"
    password = generate_password()
    user = CustomUser.objects.create_user(
        username=username,
        password=password,
        permissions_type="S",
        student=student,
    )
    user.save()
    messages.success(
        request,
        f"""Utworzono konto dla kursanta {student.full_name} - dane logowania:
                         Login: {username}
                         Hasło: {password}""",
    )
    return redirect("/students")


@requires_permissions(permission_type=["E", "A"])
def delete_account_of_student_view(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    user = get_object_or_404(CustomUser, student=student)
    user.delete()
    messages.success(
        request,
        f"""Usunięto konto kursanta {student.full_name}""",
    )
    return redirect("/students")


@requires_permissions(permission_type=["E", "A"])
def generate_new_password_for_student_view(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    user = get_object_or_404(CustomUser, student=student)
    password = generate_password()
    user.set_password(password)
    user.save()
    messages.success(
        request,
        f"""Wygenerowano nowe hasło dla kursanta {student.full_name} - dane logowania:
                         Login: {user.username}
                         Hasło: {password}""",
    )
    return redirect("/students")


class EditStudentView(View):
    template = loader.get_template("student_edit.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        context = {"student": student}
        return HttpResponse(self.template.render(context, request))

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def post(self, request, student_id):
        form = EditStudentForm(request.POST)
        if form.is_valid():
            student = get_object_or_404(Student, pk=student_id)
            student.surname = request.POST.get("surname")
            student.name = request.POST.get("name")
            student.birth_date = request.POST.get("birth_date")
            student.phone_number = request.POST.get("phone_number")
            student.email = request.POST.get("email")
            student.save()
            messages.success(request, "Zapisano zmiany")
            return redirect("/students")
        messages.error(request, "Wprowadzono niepoprawne dane")
        return redirect(f"/students/{student_id}/edit")


class CreateTheoryView(View):
    template = loader.get_template("theory_create.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request):
        instructors = Instructor.objects.filter(is_active=True)
        context = {"instructors": instructors}
        return HttpResponse(self.template.render(context, request))

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def post(self, request):
        form = NewTheoryForm(request.POST)
        if form.is_valid() and check_start_date_for_theory_course(
            form.cleaned_data["start_date"], form.cleaned_data["type"]
        ):
            theory = TheoryCourse.objects.create(
                type=form.cleaned_data["type"],
                start_date=form.cleaned_data["start_date"],
                instructor=form.cleaned_data["instructor"],
            )
            theory.save()
            messages.success(request, "Dodano nowy wykład")
            return redirect("/theories")
        messages.error(request, "Wprowadzono niepoprawne dane")
        return redirect("/theory/create")


class TheoriesView(View):
    template = loader.get_template("theories.html")

    @method_decorator(requires_permissions(permission_type=["E", "A", "I"]))
    def get(self, request):
        if request.user.permissions_type == "I":
            theories = TheoryCourse.objects.filter(
                instructor=request.user.instructor,
                start_date__gte=date.today().replace(month=date.today().month - 1),
            ).order_by("start_date")
        elif request.GET.get("instructor") != None:
            theories = self._search_results(request)
        else:
            theories = TheoryCourse.objects.all()
        instructors = Instructor.objects.filter(is_active=True)
        context = {"theories": theories, "instructors": instructors}
        return HttpResponse(self.template.render(context, request))

    def _search_results(self, request):
        theories = TheoryCourse.objects.all()
        if request.GET.get("instructor") != "":
            try:
                theories = theories.filter(instructor__pk=request.GET.get("instructor"))
            except ValueError:
                pass
        if request.GET.get("status") == "done":
            temp_theories = []
            for theory in theories:
                if theory.is_already_happened:
                    temp_theories.append(theory)
            theories = temp_theories
        elif request.GET.get("status") == "coming":
            temp_theories = []
            for theory in theories:
                if not theory.is_already_happened:
                    temp_theories.append(theory)
            theories = temp_theories
        if request.GET.get("type") == "T":
            theories = theories.filter(type="T")
        elif request.GET.get("type") == "W":
            theories = theories.filter(type="W")
        return theories


class EditTheoryView(View):
    template = loader.get_template("theory_edit.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request, theory_id):
        theory = get_object_or_404(TheoryCourse, pk=theory_id)
        instructors = Instructor.objects.filter(is_active=True)
        context = {"theory": theory, "instructors": instructors}
        return HttpResponse(self.template.render(context, request))

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def post(self, request, theory_id):
        theory = get_object_or_404(TheoryCourse, pk=theory_id)
        form = TheoryEditForm(request.POST)
        if form.is_valid() and check_start_date_for_theory_course(
            form.cleaned_data["start_date"], form.cleaned_data["type"]
        ):
            theory.type = form.cleaned_data["type"]
            theory.start_date = form.cleaned_data["start_date"]
            theory.instructor = form.cleaned_data["instructor"]
            theory.save()
            messages.success(request, "Zapisano zmiany")
            return redirect("/theories")
        else:
            messages.error(request, "Wprowadzono niepoprawne dane")
            return redirect(f"/theory/{theory_id}/edit")


@requires_permissions(permission_type=["E", "A"])
def delete_theory_view(request, theory_id):
    theory = get_object_or_404(TheoryCourse, pk=theory_id)
    if theory.is_already_happened:
        messages.error(request, "Nie można usunąć wykładu, który już się odbył")
        return redirect("/theories")
    theory.delete()
    messages.success(request, "Usunięto wykład")
    return redirect("/theories")


class VehiclesView(View):
    template = loader.get_template("vehicles.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request):
        if request.GET.get("q") != None:
            vehicles = self._search_results(request)
        else:
            vehicles = Vehicle.objects.all()
        context = {"vehicles": vehicles}
        return HttpResponse(self.template.render(context, request))

    def _search_results(self, request):
        query = request.GET.get("q")
        vehicles = Vehicle.objects.filter(
            Q(registration_number__icontains=query)
            | Q(brand__icontains=query)
            | Q(model__icontains=query)
            | Q(year_of_production__icontains=query)
        )
        if request.GET.get("type") != "all":
            temp_vehicles = []
            for vehicle in vehicles:
                if vehicle.type == request.GET.get("type"):
                    temp_vehicles.append(vehicle)
            vehicles = temp_vehicles
        if request.GET.get("gearbox") != "all":
            temp_vehicles = []
            for vehicle in vehicles:
                if vehicle.gearbox_type == request.GET.get("gearbox"):
                    temp_vehicles.append(vehicle)
            vehicles = temp_vehicles
        if request.GET.get("is_available") == "Yes":
            temp_vehicles = []
            for vehicle in vehicles:
                if vehicle.is_available:
                    temp_vehicles.append(vehicle)
            vehicles = temp_vehicles
        elif request.GET.get("is_available") == "No":
            temp_vehicles = []
            for vehicle in vehicles:
                if not vehicle.is_available:
                    temp_vehicles.append(vehicle)
            vehicles = temp_vehicles
        return vehicles


class CreateVehicleView(View):
    template = loader.get_template("vehicle_create.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request):
        return HttpResponse(self.template.render({}, request))

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def post(self, request):
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = Vehicle(
                registration_number=form.cleaned_data["registration_number"],
                brand=form.cleaned_data["brand"],
                model=form.cleaned_data["model"],
                year_of_production=form.cleaned_data["year_of_production"],
                gearbox_type=form.cleaned_data["gearbox_type"],
                type=form.cleaned_data["type"],
                is_available=True,
            )
            vehicle.save()
            messages.success(request, "Dodano pojazd")
            return redirect("/vehicles")
        else:
            messages.error(request, "Wprowadzono niepoprawne dane")
            return redirect("/vehicle/create")


class EditVehicleView(View):
    template = loader.get_template("vehicle_edit.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        context = {"vehicle": vehicle}
        return HttpResponse(self.template.render(context, request))

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def post(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle.registration_number = form.cleaned_data["registration_number"]
            vehicle.brand = form.cleaned_data["brand"]
            vehicle.model = form.cleaned_data["model"]
            vehicle.year_of_production = form.cleaned_data["year_of_production"]
            vehicle.gearbox_type = form.cleaned_data["gearbox_type"]
            vehicle.type = form.cleaned_data["type"]
            vehicle.save()
            messages.success(request, "Zapisano zmiany")
            return redirect("/vehicles")
        else:
            messages.error(request, "Wprowadzono niepoprawne dane")
            return redirect(f"/vehicle/{vehicle_id}/edit")


@requires_permissions(permission_type=["E", "A"])
def delete_vehicle_view(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    if PracticalLesson.objects.filter(vehicle=vehicle).exists():
        messages.error(
            request,
            "Nie można usunąć pojazdu, który jest przypisany do jazd praktycznych",
        )
        return redirect("/vehicles")
    vehicle.delete()
    messages.success(request, "Usunięto pojazd")
    return redirect("/vehicles")


def change_vehicle_availability_view(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    if PracticalLesson.objects.filter(vehicle=vehicle, date__gte=date.today()).exists():
        messages.error(
            request,
            "Nie można zmienić dostępności pojazdu, który jest przypisany do jazd praktycznych",
        )
        return redirect("/vehicles")
    vehicle.is_available = not vehicle.is_available
    vehicle.save()
    messages.success(request, "Zmieniono dostępność pojazdu")
    return redirect("/vehicles")


class CategoriesView(View):
    template = loader.get_template("categories.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request):
        categories = Category.objects.all()
        context = {"categories": categories}
        return HttpResponse(self.template.render(context, request))


class CreateCategoryView(View):
    template = loader.get_template("category_create.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request):
        return HttpResponse(self.template.render({}, request))

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def post(self, request):
        form = CreateCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.is_available = True
            category.save()
            messages.success(request, "Dodano kategorię")
            return redirect("/categories")
        else:
            messages.error(request, "Wprowadzono niepoprawne dane")
            return redirect("/category/create")


class EditCategoryView(View):
    template = loader.get_template("category_edit.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request, category_symbol):
        category = get_object_or_404(Category, pk=category_symbol)
        context = {"category": category}
        return HttpResponse(self.template.render(context, request))

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def post(self, request, category_symbol):
        category = get_object_or_404(Category, pk=category_symbol)
        form = EditCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category.description = form.cleaned_data["description"]
            category.price = form.cleaned_data["price"]
            category.required_practical_hours = form.cleaned_data[
                "required_practical_hours"
            ]
            category.is_discount = form.cleaned_data["is_discount"]
            category.discount_price = form.cleaned_data["discount_price"]
            if form.cleaned_data["photo"] != "default_category.jpg":
                category.photo = form.cleaned_data["photo"]
            category.save()
            messages.success(request, "Zapisano zmiany")
            return redirect("/categories")
        else:
            messages.error(request, "Wprowadzono niepoprawne dane")
            return redirect(f"/category/{category_symbol}/edit")


@requires_permissions(permission_type=["E", "A"])
def delete_category_view(request, category_symbol):
    category = get_object_or_404(Category, pk=category_symbol)
    if (
        Course.objects.filter(category=category).exists()
        or Qualification.objects.filter(category=category).exists()
    ):
        messages.error(
            request,
            "Nie można usunąć kategorii, która jest do czegoś przypisana",
        )
        return redirect("/categories")
    category.delete()
    messages.success(request, "Usunięto kategorię")
    return redirect("/categories")


@requires_permissions(permission_type=["E", "A"])
def change_category_availability_view(request, category_symbol):
    category = get_object_or_404(Category, pk=category_symbol)
    category.is_available = not category.is_available
    category.save()
    messages.success(request, "Zmieniono dostępność kategorii")
    return redirect("/categories")


class InstructorsView(View):
    template = loader.get_template("instructors.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request):
        if request.GET.get("q") != None:
            instructors = self._search_results(request)
        else:
            instructors = Instructor.objects.all()
        context = {"instructors": instructors}
        return HttpResponse(self.template.render(context, request))

    def _search_results(self, request):
        query = request.GET.get("q")
        instructors = Instructor.objects.filter(
            Q(name__icontains=query)
            | Q(surname__icontains=query)
            | Q(instructor_id__icontains=query)
            | Q(phone_number__icontains=query)
        )
        if request.GET.get("status") == "active":
            temp_instructors = []
            for instructor in instructors:
                if instructor.is_active:
                    temp_instructors.append(instructor)
            return temp_instructors
        elif request.GET.get("status") == "inactive":
            temp_instructors = []
            for instructor in instructors:
                if not instructor.is_active:
                    temp_instructors.append(instructor)
            return temp_instructors
        return instructors


class RegisterInstructorView(View):
    template = loader.get_template("register_instructor.html")

    @method_decorator(requires_permissions(permission_type=["A"]))
    def get(self, request):
        return HttpResponse(self.template.render({}, request))

    @method_decorator(requires_permissions(permission_type=["A"]))
    def post(self, request):
        form = InstructorForm(request.POST)
        if form.is_valid():
            instructor = form.save(commit=False)
            instructor.is_active = True
            instructor.save()
            next_user_id = CustomUser.objects.order_by("-pk")[0].pk + 1
            username = f"{instructor.surname.lower()[:3]}{instructor.name.lower()[:3]}{next_user_id}"
            password = generate_password()
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                permissions_type="I",
                instructor=instructor,
            )
            user.save()
            messages.success(
                request,
                f"""Dodano nowego instruktora - dane logowania:
                         Login: {username}
                         Hasło: {password}""",
            )
            return redirect("/instructors")
        else:
            messages.error(request, "Wprowadzono niepoprawne dane")
            return redirect("/register_instructor/")


class EditInstructorView(View):
    template = loader.get_template("instructor_edit.html")

    @method_decorator(requires_permissions(permission_type=["A"]))
    def get(self, request, instructor_id):
        instructor = get_object_or_404(Instructor, pk=instructor_id)
        context = {"instructor": instructor}
        return HttpResponse(self.template.render(context, request))

    @method_decorator(requires_permissions(permission_type=["A"]))
    def post(self, request, instructor_id):
        instructor = get_object_or_404(Instructor, pk=instructor_id)
        form = InstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save()
            messages.success(request, "Zapisano zmiany")
            return redirect("/instructors")
        else:
            messages.error(request, "Wprowadzono niepoprawne dane")
            return redirect(f"/instructors/{instructor_id}/edit")


@requires_permissions(permission_type=["A"])
def delete_instructor_view(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    if (
        Course.objects.filter(instructor=instructor).exists()
        or Qualification.objects.filter(instructor=instructor).exists()
        or PracticalLesson.objects.filter(instructor=instructor).exists()
        or TheoryCourse.objects.filter(instructor=instructor).exists()
    ):
        messages.error(
            request,
            "Nie można usunąć instruktora, który jest do czegoś przypisany",
        )
        return redirect("/instructors")
    instructor.delete()
    messages.success(request, "Usunięto instruktora")
    return redirect("/instructors")


@requires_permissions(permission_type=["A"])
def delete_account_of_instructor_view(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    user = get_object_or_404(CustomUser, instructor=instructor)
    user.delete()
    messages.success(request, "Usunięto konto instruktora")
    return redirect("/instructors")


@requires_permissions(permission_type=["A"])
def generate_new_password_for_instructor_view(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    user = get_object_or_404(CustomUser, instructor=instructor)
    password = generate_password()
    user.set_password(password)
    user.save()
    messages.success(
        request,
        f"""Zresetowano hasło instruktora {instructor.full_name}- dane logowania:
                    Login: {user.username}
                    Hasło: {password}""",
    )
    return redirect("/instructors")


@requires_permissions(permission_type=["A"])
def create_account_for_instructor_view(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    if CustomUser.objects.filter(instructor=instructor_id).exists():
        messages.error(request, "Konto dla tego instruktora już istnieje")
        return redirect("/instructors")
    next_user_id = CustomUser.objects.order_by("-pk")[0].pk + 1
    username = (
        f"{instructor.surname.lower()[:3]}{instructor.name.lower()[:3]}{next_user_id}"
    )
    password = generate_password()
    user = CustomUser.objects.create_user(
        username=username,
        password=password,
        permissions_type="I",
        instructor=instructor,
    )
    user.save()
    messages.success(
        request,
        f"""Utworzono konto dla instruktora {instructor.full_name} - dane logowania:
                    Login: {username}
                    Hasło: {password}""",
    )
    return redirect("/instructors")


@requires_permissions(permission_type=["E", "A"])
def change_instructor_availability_view(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    instructor.is_active = not instructor.is_active
    instructor.save()
    messages.success(request, "Zmieniono dostępność instruktora")
    return redirect("/instructors")


class QualificationsView(View):
    template = loader.get_template("qualifications.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request, instructor_id):
        instructor = get_object_or_404(Instructor, pk=instructor_id)
        qualifications = Qualification.objects.filter(instructor=instructor)
        context = {"qualifications": qualifications, "instructor": instructor}
        return HttpResponse(self.template.render(context, request))


class CreateQualificationView(View):
    template = loader.get_template("qualification_create.html")

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def get(self, request, instructor_id):
        instructor = get_object_or_404(Instructor, pk=instructor_id)
        categories = Category.objects.all()
        context = {"instructor": instructor, "categories": categories}
        return HttpResponse(self.template.render(context, request))

    @method_decorator(requires_permissions(permission_type=["E", "A"]))
    def post(self, request, instructor_id):
        instructor = get_object_or_404(Instructor, pk=instructor_id)
        form = CreateQualificationForm(request.POST)
        if form.is_valid():
            qualification = form.save(commit=False)
            if Qualification.objects.filter(
                instructor=instructor, category=qualification.category
            ).exists():
                messages.error(request, "Instruktor posiada już taką kwalifikację")
                return redirect(f"/qualification/{instructor_id}/add/")
            qualification.instructor = instructor
            if qualification.date_of_achievement >= date.today():
                messages.error(request, "Podano błędną datę")
                return redirect(f"/qualification/{instructor_id}/add/")
            qualification.save()
            messages.success(request, "Dodano kwalifikację")
            return redirect(f"/qualifications/{instructor_id}/")
        else:
            messages.error(request, "Wprowadzono niepoprawne dane")
            return redirect(f"/qualification/{instructor_id}/add/")


@requires_permissions(permission_type=["E", "A"])
def delete_qualification_view(request, qualification_id):
    qualification = get_object_or_404(Qualification, pk=qualification_id)
    qualification.delete()
    messages.success(request, "Usunięto kwalifikację")
    return redirect(f"/qualifications/{qualification.instructor.id}/")


class EmployeesView(View):
    template = loader.get_template("employees.html")

    @method_decorator(requires_permissions(permission_type=["A"]))
    def get(self, request):
        if request.GET.get("q"):
            employees = Employee.objects.filter(
                Q(name__icontains=request.GET.get("q"))
                | Q(surname__icontains=request.GET.get("q"))
            )
        else:
            employees = Employee.objects.all()
        context = {"employees": employees}
        return HttpResponse(self.template.render(context, request))


class RegisterEmployeeView(View):
    template = loader.get_template("register_employee.html")

    @method_decorator(requires_permissions(permission_type=["A"]))
    def get(self, request):
        return HttpResponse(self.template.render({}, request))

    @method_decorator(requires_permissions(permission_type=["A"]))
    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            next_user_id = CustomUser.objects.order_by("-pk")[0].pk + 1
            username = f"{employee.surname.lower()[:3]}{employee.name.lower()[:3]}{next_user_id}"
            password = generate_password()
            print(request.POST.get("is_admin"))
            if request.POST.get("is_admin") == "on":
                permissions_type = "A"
            else:
                permissions_type = "E"
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                permissions_type=permissions_type,
                employee=employee,
            )
            user.save()
            messages.success(
                request,
                f"""Dodano nowego pracownika - dane logowania:
                         Login: {username}
                         Hasło: {password}""",
            )
            return redirect("/employees/")
        else:
            messages.error(request, "Wprowadzono niepoprawne dane")
            return redirect("/register_employee/")


class EditEmployeeView(View):
    template = loader.get_template("employee_edit.html")

    @method_decorator(requires_permissions(permission_type=["A"]))
    def get(self, request, employee_id):
        employee = get_object_or_404(Employee, pk=employee_id)
        context = {"employee": employee}
        return HttpResponse(self.template.render(context, request))

    @method_decorator(requires_permissions(permission_type=["A"]))
    def post(self, request, employee_id):
        employee = get_object_or_404(Employee, pk=employee_id)
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Zaktualizowano dane pracownika")
            return redirect("/employees/")
        else:
            messages.error(request, "Wprowadzono niepoprawne dane")
            return redirect(f"/employee/{employee_id}/edit/")


@requires_permissions(permission_type=["A"])
def delete_employee_view(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.user.employee == employee:
        messages.error(request, "Nie możesz usunąć samego siebie")
        return redirect("/employees/")
    employee.delete()
    messages.success(request, "Usunięto pracownika")
    return redirect("/employees/")


@requires_permissions(permission_type=["A"])
def change_employee_permissions_type_view(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.user.employee == employee:
        messages.error(request, "Nie możesz zmienić uprawnień samemu sobie")
        return redirect("/employees/")
    user = get_object_or_404(CustomUser, employee=employee)
    if user.permissions_type == "A":
        user.permissions_type = "E"
    else:
        user.permissions_type = "A"
    user.save()
    messages.success(request, "Zmieniono uprawnienia pracownika")
    return redirect("/employees/")


@requires_permissions(permission_type=["A"])
def generate_new_password_for_employee_view(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.user.employee == employee:
        messages.error(request, "Nie możesz zmienić hasła samemu sobie")
        return redirect("/employees/")
    user = get_object_or_404(CustomUser, employee=employee)
    password = generate_password()
    user.set_password(password)
    user.save()
    messages.success(
        request,
        f"""Zmieniono hasło pracownika {employee.full_name} - dane logowania:
                 Login: {user.username}
                 Hasło: {password}""",
    )
    return redirect("/employees/")


@requires_permissions(permission_type=["A"])
def delete_account_of_employee_view(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.user.employee == employee:
        messages.error(request, "Nie możesz usunąć swojego konta")
        return redirect("/employees/")
    user = get_object_or_404(CustomUser, employee=employee)
    user.delete()
    messages.success(request, "Usunięto konto pracownika")
    return redirect("/employees/")


@requires_permissions(permission_type=["A"])
def create_account_for_employee_view(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.user.employee == employee:
        messages.error(request, "Nie możesz utworzyć konta samemu sobie")
        return redirect("/employees/")
    if CustomUser.objects.filter(employee=employee).exists():
        messages.error(request, "Konto dla tego pracownika już istnieje")
        return redirect("/employees/")
    next_user_id = CustomUser.objects.order_by("-pk")[0].pk + 1
    username = (
        f"{employee.surname.lower()[:3]}{employee.name.lower()[:3]}{next_user_id}"
    )
    password = generate_password()
    CustomUser.objects.create_user(
        username=username,
        password=password,
        permissions_type="E",
        employee=employee,
    )
    messages.success(
        request,
        f"""Utworzono konto dla pracownika {employee.full_name} - dane logowania:
                    Login: {username}
                    Hasło: {password}""",
    )
    return redirect("/employees/")
