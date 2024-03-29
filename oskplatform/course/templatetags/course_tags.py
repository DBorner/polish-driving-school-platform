from django import template
from course.models import Course
from users.models import Student, CustomUser, Qualification, Instructor, Employee

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

@register.filter(name='instructor_username')
def get_instructor_account_username(value):
    if Instructor.objects.filter(id=value).exists():
        instructor = Instructor.objects.get(id=value)
        if CustomUser.objects.filter(instructor=instructor).exists():
            return CustomUser.objects.get(instructor=instructor).username
    return None

@register.filter(name='employee_username')
def get_employer_account_username(value):
    if Employee.objects.filter(id=value).exists():
        employee = Employee.objects.get(id=value)
        if CustomUser.objects.filter(employee=employee).exists():
            return CustomUser.objects.get(employee=employee).username
    return None

@register.filter(name='is_employee_admin')
def is_employee_admin(value):
    if Employee.objects.filter(id=value).exists():
        employee = Employee.objects.get(id=value)
        if CustomUser.objects.filter(employee=employee).exists():
            if CustomUser.objects.get(employee=employee).permissions_type == 'A':
                return True
    return False

@register.filter(name='instructor_qualifications')
def get_instructor_qualifications(value):
    if Instructor.objects.filter(id=value).exists():
        instructor = Instructor.objects.get(id=value)
        return Qualification.objects.filter(instructor=instructor)
    return None