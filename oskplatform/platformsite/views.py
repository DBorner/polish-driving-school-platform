from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from course.models import Category, Vehicle, TheoryCourse
from users.models import Instructor
from users.utils import get_instructor_qualifications
from django.views import View
import datetime


class HomeView(View):
    def get(self, request):
        categories = Category.objects.all().values()
        categories = categories.filter(is_available=True)
        template = loader.get_template("home.html")
        context = {"categories": categories}
        return HttpResponse(template.render(context, request))


class CategoryView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        if category.is_available == False:
            return HttpResponse(status=404)
        template = loader.get_template("category_home.html")
        context = {
            "category": category,
        }
        return HttpResponse(template.render(context, request))


class VehiclesView(View):
    def get(self, request):
        template = loader.get_template("vehicles_home.html")
        vehicles = Vehicle.objects.all().values()
        vehicles = vehicles.filter(is_available=True).exclude(type__startswith="P")
        context = {"vehicles": vehicles}
        return HttpResponse(template.render(context, request))


class InstructorsView(View):
    def get(self, request):
        template = loader.get_template("instructors_home.html")
        instructors = Instructor.objects.all().values()
        instructors = instructors.filter(is_active=True)
        instructors_qualifications = []
        for instructor in instructors:
            instructors_qualifications.append(
                (instructor, get_instructor_qualifications(instructor["id"]))
            )
        context = {"instructors": instructors_qualifications}
        return HttpResponse(template.render(context, request))


class TheorysView(View):
    def get(self, request):
        template = loader.get_template("theories_home.html")
        theories = (
            TheoryCourse.objects.all()
            .values()
            .filter(start_date__gte=datetime.date.today())
        )
        theories = theories.exclude(
            start_date__gt=datetime.date.today() + datetime.timedelta(days=30)
        )
        instructors = Instructor.objects.all().values()
        data = []
        for theory in theories:
            data.append((theory, instructors.get(pk=theory["instructor_id"])))
        context = {"theories": data}
        return HttpResponse(template.render(context, request))
