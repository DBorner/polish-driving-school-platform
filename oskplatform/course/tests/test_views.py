from django.test import TestCase
from datetime import date
from users.models import Student, Instructor, Qualification, CustomUser
from course.models import Category, Vehicle, Course, TheoryCourse, PracticalLesson
from datetime import datetime, date
from model_bakery import baker
from django.urls import reverse

class ProfileSettingsViewTest(TestCase):
    def setUp(self):
        self.url = reverse('profile_settings')
        self.user = baker.make(CustomUser)
        self.client.force_login(self.user)

    def test_profile_settings_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_settings.html')
        
    def test_instructor_profile_settings_view_get(self):
        self.user.permissions_type = 'I'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_settings.html')
        
    def test_admin_profile_settings_view_get(self):
        self.user.permissions_type = 'A'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_settings.html')
        
    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertTemplateNotUsed(response, 'profile_settings.html')
        
    def test_profile_settings_view_post(self):
        new_password = "khFLkao!124124!aflkj!"
        new_data = {
            'new_password1': new_password,
            'new_password2': new_password,
        }
        response = self.client.post(self.url, new_data)
        self.assertEqual(response.status_code, 302)
        
    def test_wrong_password(self):
        response = self.client.post(self.url, {'new_password1': '123', 'new_password2': '123'})
        self.assertEqual(response.status_code, 302)
        
class UpcomingLessonsViewTest(TestCase):
    def setUp(self):
        self.url = reverse('upcoming_lessons')
        self.student = baker.make(Student)
        self.category = baker.make(Category, required_practical_hours=10)
        self.course = baker.make(Course, category=self.category, student=self.student)
        self.practical_lesson = baker.make(PracticalLesson, course=self.course, num_of_hours=10)
        self.user = baker.make(CustomUser, student=self.student)
        self.client.force_login(self.user)
        
    def test_upcoming_lessons_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upcoming_lessons.html')
        
    def test_instructor_upcoming_lessons_view_get(self):
        self.user.permissions_type = 'I'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upcoming_lessons.html')
        
    def test_employee_upcoming_lessons_view_get(self):
        self.user.permissions_type = 'E'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upcoming_lessons.html')
        
    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertTemplateNotUsed(response, 'upcoming_lessons.html')

class CoursesViewTest(TestCase):
    def setUp(self):
        self.url = reverse('courses')
        self.student = baker.make(Student)
        self.category = baker.make(Category, required_practical_hours=10)
        self.course = baker.make(Course, category=self.category, student=self.student)
        self.practical_lesson = baker.make(PracticalLesson, course=self.course, num_of_hours=10)
        self.user = baker.make(CustomUser, student=self.student)
        self.client.force_login(self.user)
        
    def test_courses_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')
        
    def test_instructor_courses_view_get(self):
        self.user.permissions_type = 'I'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')
        
    def test_employee_courses_view_get(self):
        self.user.permissions_type = 'E'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')
        
    def test_with_student_id(self):
        response = self.client.get('/students/0/courses/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')
        
    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertTemplateNotUsed(response, 'courses.html')

class CourseDetailViewTest(TestCase):
    def setUp(self):
        self.student = baker.make(Student)
        self.category = baker.make(Category, required_practical_hours=10)
        self.course = baker.make(Course, category=self.category, student=self.student)
        self.practical_lesson = baker.make(PracticalLesson, course=self.course, num_of_hours=10)
        self.url = '/courses/1/'
        self.user = baker.make(CustomUser, student=self.student)
        self.client.force_login(self.user)
        
    def test_course_detail_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_detail.html')
        
    def test_instructor_course_detail_view_get(self):
        self.user.permissions_type = 'I'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_detail.html')
        
    def test_employee_course_detail_view_get(self):
        self.user.permissions_type = 'E'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_detail.html')
        
    def test_another_student_course_detail_view_get(self):
        self.user.permissions_type = 'S'
        self.course.student = baker.make(Student)
        self.course.save()
        self.user.save()    
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'course_detail.html')
        
    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertTemplateNotUsed(response, 'course_detail.html')
        
class PracticalDetailViewTest(TestCase):
    def setUp(self):
        self.student = baker.make(Student)
        self.category = baker.make(Category, required_practical_hours=10)
        self.course = baker.make(Course, category=self.category, student=self.student)
        self.practical_lesson = baker.make(PracticalLesson, course=self.course, num_of_hours=10)
        self.url = "/practical/1/"
        self.user = baker.make(CustomUser, student=self.student)
        self.client.force_login(self.user)
        
    def test_practical_detail_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practical_detail.html')
        
    def test_instructor_practical_detail_view_get(self):
        self.user.permissions_type = 'I'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practical_detail.html')
        
    def test_employee_practical_detail_view_get(self):
        self.user.permissions_type = 'E'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practical_detail.html')
        
    def test_another_student_practical_detail_view_get(self):
        self.user.permissions_type = 'S'
        self.course.student = baker.make(Student)
        self.course.save()
        self.user.save()    
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'practical_detail.html')
        
    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertTemplateNotUsed(response, 'practical_detail.html')
        
class ChangePracticalLessonStatusTest(TestCase):
    def setUp(self):
        self.student = baker.make(Student)
        self.category = baker.make(Category, required_practical_hours=10)
        self.course = baker.make(Course, category=self.category, student=self.student)
        self.practical_lesson = baker.make(PracticalLesson, course=self.course, num_of_hours=10)
        self.url = "/practical/1/change_status/"
        self.user = baker.make(CustomUser, student=self.student, permissions_type='E')
        self.client.force_login(self.user)
        
        
    def test_change_practical_lesson_status(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PracticalLesson.objects.get(pk=1).is_cancelled, True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PracticalLesson.objects.get(pk=1).is_cancelled, False)
        
    def test_change_with_wrong_permissions(self):
        self.user.permissions_type = 'S'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PracticalLesson.objects.get(pk=1).is_cancelled, False)
    
    def test_instructor_that_not_his_lesson(self):
        self.user.permissions_type = 'I'
        self.user.save()
        self.course.instructor = baker.make(Instructor)
        self.course.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PracticalLesson.objects.get(pk=1).is_cancelled, False)
        
class DeletePracticalLessonTest(TestCase):
    def setUp(self):
        self.student = baker.make(Student)
        self.category = baker.make(Category, required_practical_hours=10)
        self.course = baker.make(Course, category=self.category, student=self.student)
        self.practical_lesson = baker.make(PracticalLesson, course=self.course, num_of_hours=10)
        self.url = "/practical/1/delete/"
        self.user = baker.make(CustomUser, student=self.student, permissions_type='E')
        self.client.force_login(self.user)
        
        
    def test_delete_practical_lesson(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PracticalLesson.objects.filter(pk=1).exists(), False)
        
    def test_delete_with_wrong_permissions(self):
        self.user.permissions_type = 'S'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PracticalLesson.objects.filter(pk=1).exists(), True)
    
    def test_instructor_that_not_his_lesson(self):
        self.user.permissions_type = 'I'
        self.user.save()
        self.course.instructor = baker.make(Instructor)
        self.course.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PracticalLesson.objects.filter(pk=1).exists(), True)
        
    def test_delete_lesson_that_has_happened(self):
        self.practical_lesson.date = date.today().replace(year=date.today().year-1)
        self.practical_lesson.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PracticalLesson.objects.filter(pk=1).exists(), True)

