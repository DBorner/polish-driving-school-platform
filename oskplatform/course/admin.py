from django.contrib import admin
from .models import Vehicle, Category, Course, TheoryCourse, PracticalLesson


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(TheoryCourse)
admin.site.register(PracticalLesson)
admin.site.register(Vehicle)