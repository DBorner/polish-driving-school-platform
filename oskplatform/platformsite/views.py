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