from .models import TheoryCourse
from users.models import Qualification, Instructor, Student
from course.models import Course
import datetime
from django.contrib import messages
from django.shortcuts import redirect
from password_generator import PasswordGenerator


def check_instructor_qualifications(instructor, category):
    if category == None or instructor == None:
        return True
    qualifications = Qualification.objects.filter(instructor=instructor)
    for qualification in qualifications:
        if qualification.category == category:
            return True
    return False


def get_course_dates(theory_id):
    course = TheoryCourse.objects.get(pk=theory_id)
    if course == None:
        return None
    dates = []
    if course.type == "T":
        if course.start_date.weekday() != 0:
            print("Wrong start date")
            return None
        dates.append((course.start_date, ("8:00", "14:00")))
        dates.append(
            (course.start_date + datetime.timedelta(days=1), ("8:00", "14:00"))
        )
        dates.append(
            (course.start_date + datetime.timedelta(days=2), ("8:00", "14:00"))
        )
        dates.append(
            (course.start_date + datetime.timedelta(days=3), ("8:00", "14:00"))
        )
        dates.append(
            (course.start_date + datetime.timedelta(days=4), ("8:00", "14:00"))
        )
        return dates
    else:
        if course.start_date.weekday() != 5:
            print("Wrong start date")
            return None
        dates.append((course.start_date, ("8:00", "16:00")))
        dates.append(
            (course.start_date + datetime.timedelta(days=1), ("9:00", "16:00"))
        )
        dates.append(
            (course.start_date + datetime.timedelta(days=7), ("8:00", "16:00"))
        )
        dates.append(
            (course.start_date + datetime.timedelta(days=8), ("9:00", "16:00"))
        )
        return dates


def is_student_active(student: Student):
    if Course.objects.filter(student=student, course_status="R").exists():
        return True
    return False


def requires_permissions(
    permission_type: list() = ["S"],
    redirect_url="/",
    redirect_message="Nie posiadasz wystarczająch uprawnień do wykonania tej akcji",
):
    def decorator(view_func):
        def _wrapper_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.permissions_type in permission_type:
                    return view_func(request, *args, **kwargs)
            messages.error(request, redirect_message)
            return redirect(redirect_url)

        return _wrapper_view

    return decorator


def generate_password():
    pwo = PasswordGenerator()
    pwo.minlen = 6
    pwo.maxlen = 6
    return pwo.generate()
