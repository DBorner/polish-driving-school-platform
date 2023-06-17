from django.test import TestCase
from datetime import date
from users.models import Student, Instructor
from course.models import Category, Vehicle, Course, TheoryCourse, PracticalLesson
from datetime import datetime


class VehicleModelTest(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            brand="Ford",
            model="Focus",
            registration_number="KR12345",
            year_of_production=2010,
        )

    def test_str_method(self):
        self.assertEqual(str(self.vehicle), "KR12345 - SO")

    def test_get_type(self):
        self.assertEqual(self.vehicle.get_type(), "Samochód osobowy")

    def test_get_gearbox(self):
        self.assertEqual(self.vehicle.get_gearbox(), "Manualna")


class CourseModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
        )
        self.instructor = Instructor.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
            phone_number="123456789",
            instructor_id="123456789",
        )
        self.category = Category.objects.create(
            symbol="AA", price=100, required_practical_hours=10
        )
        self.course = Course.objects.create(
            student=self.student,
            pkk_number="123456789",
            cost=1000,
            start_date=date(2020, 1, 1),
            instructor=self.instructor,
            category=self.category,
        )

    def test_str_method(self):
        self.assertEqual(str(self.course), "Smith John (AA)")

    def test_is_instructor_assigned(self):
        self.assertTrue(self.course.is_instructor_assigned)

    def test_is_instructor_assigned_with_no_instructor(self):
        self.course.instructor = None
        self.assertFalse(self.course.is_instructor_assigned)

    def test_get_status(self):
        self.assertEqual(self.course.get_status, "Rozpoczęty")


class TheoryCourseModelTest(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
            phone_number="123456789",
            instructor_id="123456789",
        )
        self.theory_course = TheoryCourse.objects.create(
            instructor=self.instructor,
            start_date=date.today().replace(day=date.today().day + 1),
        )
        self.theory_course2 = TheoryCourse.objects.create(
            instructor=self.instructor,
            start_date=date.today().replace(day=date.today().day - 1),
        )

    def test_str_method(self):
        self.assertEqual(
            str(self.theory_course), f"1 - {self.theory_course.start_date} (T)"
        )

    def test_is_alreadu_happened(self):
        self.assertFalse(self.theory_course.is_already_happened)
        self.assertTrue(self.theory_course2.is_already_happened)

    def test_get_type(self):
        self.assertEqual(self.theory_course.get_type, "Tygodniowy")


class PracticalLessonModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
        )
        self.instructor = Instructor.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
            phone_number="123456789",
            instructor_id="123456789",
        )
        self.category = Category.objects.create(
            symbol="AA", price=100, required_practical_hours=10
        )
        self.course = Course.objects.create(
            student=self.student,
            pkk_number="123456789",
            cost=1000,
            start_date=date(2020, 1, 1),
            instructor=self.instructor,
            category=self.category,
        )
        self.practical_lesson = PracticalLesson.objects.create(
            course=self.course,
            date=date.today().replace(day=date.today().day + 1),
            start_time="10:00",
            num_of_hours=1,
            instructor=self.instructor,
        )
        self.practical_lesson2 = PracticalLesson.objects.create(
            course=self.course,
            date=date.today().replace(day=date.today().day - 1),
            start_time="10:00",
            num_of_hours=1,
            instructor=self.instructor,
        )

    def test_str_method(self):
        self.assertEqual(
            str(self.practical_lesson), f"{self.practical_lesson.id} - 123456789 {date.today().replace(day=date.today().day + 1)} (10:00)"
        )

    def test_is_alreadu_happened(self):
        self.assertFalse(self.practical_lesson.has_already_happened)
        self.assertTrue(self.practical_lesson2.has_already_happened)

    def test_is_paid(self):
        self.assertFalse(self.practical_lesson.is_paid)
        self.practical_lesson.cost = 100
        self.assertTrue(self.practical_lesson.is_paid)

    def test_get_end_time(self):
        self.assertEqual(self.practical_lesson.get_end_time, datetime(datetime.today().year, datetime.today().month, datetime.today().day+1, 11, 0) )

    def test_is_number_of_km_filled(self):
        self.assertFalse(self.practical_lesson.is_number_of_km_filled)
        self.practical_lesson.num_of_km = 2
        self.assertTrue(self.practical_lesson.is_number_of_km_filled)

    def test_is_vehicle_filled(self):
        self.assertFalse(self.practical_lesson.is_vehicle_filled)
        self.practical_lesson.vehicle = Vehicle.objects.create(
            brand="Ford",
            model="Focus",
            registration_number="KR12345",
            year_of_production=2010,
        )
        self.assertTrue(self.practical_lesson.is_vehicle_filled)
