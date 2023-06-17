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

class EditPracticalLessonViewTest(TestCase):
    def setUp(self):
        self.student = baker.make(Student)
        self.category = baker.make(Category, required_practical_hours=10)
        self.course = baker.make(Course, category=self.category, student=self.student)
        self.practical_lesson = baker.make(PracticalLesson, course=self.course, num_of_hours=10)
        self.url = "/practical/1/edit/"
        self.user = baker.make(CustomUser, student=self.student, permissions_type='E')
        self.client.force_login(self.user)
        self.instructor = baker.make(Instructor)
        
        
    def test_edit_practical_lesson(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practical_edit.html')
        
    def test_edit_with_wrong_permissions(self):
        self.user.permissions_type = 'S'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'practical_edit.html')
    
    def test_instructor_that_not_his_lesson(self):
        self.user.permissions_type = 'I'
        self.user.save()
        self.practical_lesson.instructor = baker.make(Instructor)
        self.practical_lesson.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'practical_edit.html')
    
    def test_post_edit_practical_lesson(self):
        data = {
            'date': date.today(),
            'num_of_hours': 5,
            'start_time': datetime.now().time(),
            'instructor': self.instructor.id,
            'cost': 100,
            'num_of_km': 5,
            
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PracticalLesson.objects.get(pk=1).num_of_hours, 5)
    
    def test_post_wrong_data(self):
        data = {
            'date': date.today(),
            'num_of_hours': 5,            
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PracticalLesson.objects.get(pk=1).num_of_hours, 10)
        
class CreatePracticalLessonView(TestCase):
    def setUp(self):
        self.student = baker.make(Student)
        self.category = baker.make(Category, required_practical_hours=10)
        self.course = baker.make(Course, category=self.category, student=self.student)
        self.url = "/practical/create/"
        self.instructor = baker.make(Instructor)
        self.qualification = baker.make(Qualification, instructor=self.instructor, category=self.category)
        self.user = baker.make(CustomUser, instructor=self.instructor, permissions_type='I')
        self.client.force_login(self.user)
        
        
    def test_create_practical_lesson(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practical_create.html')
        
    def test_create_with_wrong_permissions(self):
        self.user.permissions_type = 'S'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'practical_create.html')
    
    def test_post_create_practical_lesson(self):
        data = {
            "course": self.course.id,
            "date": date.today(),
            "start_time": datetime.now().time(),
            "num_of_hours": 5,
            "num_of_km": 5,
            "cost": 100,    
            
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PracticalLesson.objects.filter(course=self.course).count(), 1)
    
    def test_post_wrong_data(self):
        data = {
            "course": self.course.id,
            "date": date.today(),
            "start_time": datetime.now().time(),       
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PracticalLesson.objects.filter(course=self.course).count(), 0)

class CreateCourseView(TestCase):
    def setUp(self):
        self.student = baker.make(Student)
        self.instructor = baker.make(Instructor)
        self.category = baker.make(Category, required_practical_hours=10)
        self.url = "/courses/create/"
        self.user = baker.make(CustomUser, student=self.student, permissions_type='E')
        self.client.force_login(self.user)
        
        
    def test_create_course(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_create.html')
        
    def test_create_with_wrong_permissions(self):
        self.user.permissions_type = 'I'
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'course_create.html')
    
    def test_post_create_course(self):
        data = {
            'pkk_number': '12345123451234512345',
            'cost': 100.0,
            'category': self.category.symbol,
            'student': self.student.id,
            'instructor': "",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Course.objects.filter(student=self.student).count(), 1)
        
    def test_post_wrong_pkk_number(self):
        data = {
            'pkk_number': '123451234512345123',
            'cost': 100.0,
            'category': self.category.symbol,
            'student': self.student.id,
            'instructor': "",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Course.objects.filter(student=self.student).count(), 0)
        
    def test_post_wrong_data(self):
        data = {
            'cost': 100,
            'category': self.category.symbol,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Course.objects.filter(student=self.student).count(), 0)

class EditCourseView(TestCase):
    def setUp(self):
        self.student = baker.make(Student)
        self.instructor = baker.make(Instructor)
        self.category = baker.make(Category, required_practical_hours=10)
        self.course = baker.make(Course, category=self.category, student=self.student)
        self.url = "/courses/edit/1/"
        self.user = baker.make(CustomUser, student=self.student, permissions_type='E')
        self.client.force_login(self.user)
    