from django.contrib import admin
from django.urls import path
from users import views as user_views
from platformsite import views as platform_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_info/', user_views.user_info),
    path('', platform_views.home),
]
