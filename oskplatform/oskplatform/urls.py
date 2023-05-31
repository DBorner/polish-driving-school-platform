from django.contrib import admin
from django.urls import path
from users import views as user_views
from platformsite import views as platform_views
from course import views as course_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('category/<str:category_id>/', platform_views.category),
    path('vehicles/', platform_views.vehicles),
    path('instructors/', platform_views.instructors),
    path('theorys/', platform_views.theorys),
    path('login/', user_views.login_view),
    path('logout/', user_views.logout_view),
    path('panel/', course_views.panel_view),
    path('students/', course_views.students_view),
    path('register_student/', course_views.register_student_view),
    path('upcoming_lessons/', course_views.upcoming_lessons_view),
    path('profile_settings/', course_views.profile_settings_view),
    path('courses/', course_views.courses_view),
    path('courses/<int:course_id>/', course_views.course_detail_view),
    path('courses/create/', course_views.create_course_view),
    path('courses/create/<int:student_id>/', course_views.create_course_view),
    path('courses/<int:course_id>/edit/', course_views.edit_course_view),
    path('practical/<int:practical_id>/', course_views.practical_detail_view),
    path('practical/<int:practical_id>/change_status/', course_views.change_practical_lesson_status_view),
    path('practical/<int:practical_id>/edit/', course_views.edit_practical_lesson_view),
    path('practical/<int:practical_id>/delete/', course_views.delete_practical_lesson_view),
    path('practical/create/', course_views.create_practical_lesson_view),
    path('practical/create/<int:course_id>/', course_views.create_practical_lesson_view),
    path('', platform_views.home),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
