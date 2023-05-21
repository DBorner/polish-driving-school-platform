from django.contrib import admin
from .models import student, instructor, employee, qualification

admin.site.register(student)
admin.site.register(instructor)
admin.site.register(employee)
admin.site.register(qualification)