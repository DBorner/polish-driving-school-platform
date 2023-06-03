from django.contrib import admin
from django.urls import path
from users import views as user_views
from platformsite import views as platform_views
from course import views as course_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('category/<str:category_id>/', platform_views.CategoryView.as_view()),
    path('vehicles/', platform_views.VehiclesView.as_view()),
    path('instructors/', platform_views.InstructorsView.as_view()),
    path('theorys/', platform_views.TheorysView.as_view()),
    path('login/', user_views.LoginView.as_view()),
    path('logout/', user_views.logout_view),
    path('panel/', course_views.PanelView.as_view()),
    path('students/', course_views.StudentsView.as_view(), name='students'),
    path('students/<int:student_id>/edit', course_views.EditStudentView.as_view()),
    path('students/<int:student_id>/create_account', course_views.create_account_for_student_view),
    path('students/<int:student_id>/delete_account', course_views.delete_account_of_student_view),
    path('students/<int:student_id>/generate_password', course_views.generate_new_password_for_student_view),
    path('students/<int:student_id>/courses/', course_views.CoursesView.as_view()),
    path('register_student/', course_views.RegisterStudentView.as_view()),
    path('upcoming_lessons/', course_views.UpcomingLessonsView.as_view()),
    path('profile_settings/', course_views.ProfileSettingsView.as_view()),
    path('courses/', course_views.CoursesView.as_view()),
    path('courses/<int:course_id>/', course_views.CourseDetailView.as_view()),
    path('courses/create/', course_views.CreateCourseView.as_view()),
    path('courses/create/<int:student_id>/', course_views.CreateCourseView.as_view()),
    path('courses/<int:course_id>/edit/', course_views.EditCourseView.as_view()),
    path('practical/<int:practical_id>/', course_views.PracticalDetailView.as_view()),
    path('practical/<int:practical_id>/change_status/', course_views.change_practical_lesson_status_view),
    path('practical/<int:practical_id>/edit/', course_views.EditPracticalLessonView.as_view()),
    path('practical/<int:practical_id>/delete/', course_views.delete_practical_lesson_view),
    path('practical/create/', course_views.CreatePracticalLessonView.as_view()),
    path('practical/create/<int:course_id>/', course_views.CreatePracticalLessonView.as_view()),
    path('', platform_views.HomeView.as_view(), name='home'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
