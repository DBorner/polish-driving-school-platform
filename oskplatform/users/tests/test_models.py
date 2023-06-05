from django.test import TestCase
from datetime import date
from users.models import Student, Instructor, Employee, Qualification, CustomUser
from course.models import Category


class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
            phone_number="123456789",
            email="john@example.com",
        )

    def test_str_method(self):
        self.assertEqual(str(self.student), "1 - Smith John")

    def test_full_name_property(self):
        self.assertEqual(self.student.full_name, "Smith John")


class InstructorModelTest(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
            phone_number="123456789",
            instructor_id="123456789",
        )

    def test_str_method(self):
        self.assertEqual(str(self.instructor), "1 - Smith John")

    def test_full_name_property(self):
        self.assertEqual(self.instructor.full_name, "Smith John")


class EmployeeModelTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
        )

    def test_str_method(self):
        self.assertEqual(str(self.employee), "1 - Smith John")

    def test_full_name_property(self):
        self.assertEqual(self.employee.full_name, "Smith John")


class QualificationModelTest(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
            phone_number="123456789",
            instructor_id="123456789",
        )
        self.category = Category.objects.create(
            symbol="A", price=100, required_practical_hours=10
        )
        self.qualification = Qualification.objects.create(
            instructor=self.instructor,
            category=self.category,
            date_of_achievement=date(2020, 1, 1),
        )

    def test_str_method(self):
        self.assertEqual(str(self.qualification), "(1 - Smith John) - (A)")


class CustomUserMenagerTest(TestCase):
    def test_no_username(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(username=None, email="", password="test")

    def test_user_creation(self):
        user = CustomUser.objects.create_user(
            username="test", email="", password="test"
        )
        self.assertEqual(user.username, "test")
        self.assertEqual(user.check_password("test"), True)
