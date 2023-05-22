from django.contrib import admin
from django.urls import path
from users import views as user_views
from platformsite import views as platform_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_info/', user_views.user_info),
    path('category/<str:category_id>/', platform_views.category),
    path('vehicles/', platform_views.vehicles),
    path('', platform_views.home),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
