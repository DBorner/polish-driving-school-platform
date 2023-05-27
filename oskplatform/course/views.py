from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def panel_view(request):
    template = loader.get_template('panel.html')
    return HttpResponse(template.render({}, request))
