from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from course.models import Category, Vehicle, TheoryCourse
from course.utils import get_course_dates
from users.models import Instructor
from users.utils import get_inctructor_qualifications
import datetime


def home(request):
    categories = Category.objects.all().values()
    categories = categories.filter(is_available=True)
    template = loader.get_template('home.html')
    context = {
        'categories': categories
    }
    return HttpResponse(template.render(context, request))

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if(category.is_available == False):
        return render(request, '404.html')
    template = loader.get_template('category.html')
    context = {
        'category': category,
    }
    return HttpResponse(template.render(context, request))

def vehicles(request):
    template = loader.get_template('vehicles.html')
    vehicles = Vehicle.objects.all().values()
    vehicles = vehicles.filter(is_available=True).exclude(type__startswith='P')
    context = {
        'vehicles': vehicles
    }
    return HttpResponse(template.render(context, request))

def instructors(request):
    template = loader.get_template('instructors.html')
    instructors = Instructor.objects.all().values()
    instructors = instructors.filter(is_active=True)
    instructors_qualifications = []
    for instructor in instructors:
        instructors_qualifications.append((instructor, get_inctructor_qualifications(instructor['id'])))
    context = {
        'instructors': instructors_qualifications
    }
    return HttpResponse(template.render(context, request))

def theorys(request):
    template = loader.get_template('theories.html')
    theories = TheoryCourse.objects.all().values().filter(start_date__gte=datetime.date.today())
    theories = theories.exclude(start_date__gt=datetime.date.today() + datetime.timedelta(days=30))
    instructors = Instructor.objects.all().values()
    data = []
    for theory in theories:
        data.append((theory, instructors.get(pk=theory['instructor_id'])))
    context = {
        'theories': data
    }
    return HttpResponse(template.render(context, request))