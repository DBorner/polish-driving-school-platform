from django.http import HttpResponse
from django.template import loader
from course.models import Category


def home(request):
    categories = Category.objects.all().values()
    template = loader.get_template('home.html')
    print(categories)
    context = {
        'categories': categories
    }
    return HttpResponse(template.render(context, request))

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    template = loader.get_template('category.html')
    context = {
        'category': category,
    }
    print(category.photo.url)
    return HttpResponse(template.render(context, request))