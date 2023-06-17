from django.test import TestCase
from course.models import Course, Category
from users.models import Student, CustomUser, Qualification, Instructor, Employee
from datetime import date
from course.templatetags.course_tags import is_student_active, get_student_account_username, get_instructor_account_username, get_employer_account_username, is_employee_admin, get_instructor_qualifications

class IsStudentActiveTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
        )
        self.category = Category.objects.create(
            symbol="AA", price=100, required_practical_hours=10
        )
        self.course = Course.objects.create(
            student=self.student,
            pkk_number="123456789",
            cost=1000,
            start_date=date(2020, 1, 1),
            category=self.category,
        )
        
    def test_is_student_active(self):
        self.assertTrue(is_student_active(self.student.id))
        
    def test_is_student_active_with_no_course(self):
        self.course.delete()
        self.assertFalse(is_student_active(self.student.id))
        
    def test_wrong_id(self):
        self.assertFalse(is_student_active(100))
        
    def test_wrong_type(self):
        self.assertFalse(is_student_active("100"))
        
class GetStudentAccountUsernameTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
        )
        self.CustomUser = CustomUser.objects.create(
            username="test",
            student=self.student,
        )
        
    def test_get_student_account_username(self):
        self.assertEqual(get_student_account_username(self.student.id), "test")
        
    def test_student_has_no_account(self):
        self.CustomUser.delete()
        self.assertEqual(get_student_account_username(self.student.id), None)
        
    def test_wrong_id(self):
        self.assertEqual(get_student_account_username(100), None)
        
    def test_wrong_type(self):
        self.assertEqual(get_student_account_username("100"), None)
        
class GetInstructorAccountUsernameTest(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
        )
        self.CustomUser = CustomUser.objects.create(
            username="test",
            instructor=self.instructor,
        )
        
    def test_get_instructor_account_username(self):
        self.assertEqual(get_instructor_account_username(self.instructor.id), "test")
        
    def test_instructor_has_no_account(self):
        self.CustomUser.delete()
        self.assertEqual(get_instructor_account_username(self.instructor.id), None)
        
    def test_wrong_id(self):
        self.assertEqual(get_instructor_account_username(100), None)
        
    def test_wrong_type(self):
        self.assertEqual(get_instructor_account_username("100"), None)
        
class GetEmployerAccountUsernameTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
        )
        self.CustomUser = CustomUser.objects.create(
            username="test",
            employee=self.employee,
        )
        
    def test_get_employee_account_username(self):
        self.assertEqual(get_employer_account_username(self.employee.id), "test")
        
    def test_employee_has_no_account(self):
        self.CustomUser.delete()
        self.assertEqual(get_employer_account_username(self.employee.id), None)
        
    def test_wrong_id(self):
        self.assertEqual(get_employer_account_username(100), None)
        
    def test_wrong_type(self):
        self.assertEqual(get_employer_account_username("100"), None)
        
class IsEmployeeAdminTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
        )
        self.CustomUser = CustomUser.objects.create(
            username="test",
            employee=self.employee,
            permissions_type="A"
        )
    
    def test_is_employee_admin(self):
        self.assertTrue(is_employee_admin(self.employee.id))
        
    def test_normal_employee(self):
        self.CustomUser.permissions_type = "E"
        self.CustomUser.save()
        self.assertFalse(is_employee_admin(self.employee.id))
    
    def test_wrong_id(self):
        self.assertFalse(is_employee_admin(100))
        
    def test_wrong_type(self):
        self.assertFalse(is_employee_admin("100"))

class GetInstructorQualificationsTest(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
        )
        self.category = Category.objects.create(
            symbol="AA", price=100, required_practical_hours=10
        )
        self.qualification = Qualification.objects.create(
            instructor=self.instructor,
            category=self.category,
            date_of_achievement=date(2020, 1, 1)
        )
    
    def test_get_instructor_qualifications(self):
        self.assertEqual(get_instructor_qualifications(self.instructor.id)[0], self.qualification)
        
    def test_instructor_has_no_qualifications(self):
        self.qualification.delete()
        self.assertEqual(len(get_instructor_qualifications(self.instructor.id)), 0)
        
    def test_wrong_id(self):
        self.assertEqual(get_instructor_qualifications(100), None)
    
    def test_wrong_type(self):
        self.assertEqual(get_instructor_qualifications("100"), None)
            