from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from course.models import Category


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