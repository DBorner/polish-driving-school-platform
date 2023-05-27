from django.contrib import admin
from django.urls import path
from users import views as user_views
from platformsite import views as platform_views
from course import views as course_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_info/', user_views.user_info),
    path('category/<str:category_id>/', platform_views.category),
    path('vehicles/', platform_views.vehicles),
    path('instructors/', platform_views.instructors),
    path('theorys/', platform_views.theorys),
    path('login/', user_views.login_view),
    path('logout/', user_views.logout_view),
    path('panel/', course_views.panel_view),
    path('register_student/', course_views.register_student_view),
    path('upcoming_lessons/', course_views.upcoming_lessons_view),
    path('', platform_views.home),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
