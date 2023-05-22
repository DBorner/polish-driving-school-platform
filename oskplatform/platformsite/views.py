from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from course.models import Category, Vehicle
from users.models import Instructor
from users.utils import get_inctructor_qualifications


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