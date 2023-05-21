from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Instructor, Employee, Qualification, CustomUser

admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Employee)
admin.site.register(Qualification)
admin.site.register(CustomUser)