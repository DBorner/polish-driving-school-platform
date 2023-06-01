from django import template
from course.models import Course
from users.models import Student, CustomUser

register = template.Library()

@register.filter(name='is_student_active')
def is_student_active(value):
    if Student.objects.filter(id=value).exists():
        student = Student.objects.get(id=value)
        if Course.objects.filter(student=student, course_status='R').exists():
            return True
    return False

@register.filter(name='student_username')
def get_student_account_username(value):
    if Student.objects.filter(id=value).exists():
        student = Student.objects.get(id=value)
        if CustomUser.objects.filter(student=student).exists():
            return CustomUser.objects.get(student=student).username
    return None