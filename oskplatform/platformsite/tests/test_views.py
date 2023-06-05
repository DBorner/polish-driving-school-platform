from django.test import TestCase
from users.models import Instructor, Qualification
from course.models import Category, Vehicle, TheoryCourse
from datetime import date


class HomeViewTest(TestCase):
    def test_get_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class CategoryViewTest(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(
            symbol="A", price=100, required_practical_hours=10
        )
        self.category2 = Category.objects.create(
            symbol="B", price=100, required_practical_hours=10, is_available=False
        )

    def test_get_category_with_available_category(self):
        response = self.client.get("/home/category/A/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A")

    def test_get_category_with_inavailable_category(self):
        response = self.client.get("/home/category/B/")
        self.assertEqual(response.status_code, 404)

    def test_fake_category(self):
        response = self.client.get("/home/category/C/")
        self.assertEqual(response.status_code, 404)


class VehiclesViewTest(TestCase):
    def setUp(self):
        self.vehicle1 = Vehicle.objects.create(
            registration_number="123456789", brand="Test1"
        )
        self.vehicle2 = Vehicle.objects.create(
            registration_number="987654321", brand="Test2", is_available=False
        )

    def test_get_vehicles(self):
        response = self.client.get("/home/vehicles/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test1")
        self.assertNotContains(response, "Test2")


class InstructorsView(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
            phone_number="123456789",
            instructor_id="123456789",
        )
        self.category1 = Category.objects.create(
            symbol="AA", price=100, required_practical_hours=10
        )
        self.category2 = Category.objects.create(
            symbol="BB", price=100, required_practical_hours=10
        )
        self.qualification = Qualification.objects.create(
            instructor=self.instructor,
            category=self.category1,
            date_of_achievement=date(2020, 1, 1),
        )
        self.instructor2 = Instructor.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
            phone_number="123456789",
            instructor_id="123456789",
            is_active=False,
        )

    def test_instructors_view(self):
        response = self.client.get("/home/instructors/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Smith")
        self.assertContains(response, "AA")
        self.assertNotContains(response, "Smith2")
        self.assertNotContains(response, "BB")


class TheorysViewTest(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
            phone_number="123456789",
            instructor_id="123456789",
        )
        self.theory1 = TheoryCourse.objects.create(
            instructor=self.instructor,
            start_date=date.today().replace(year=date.today().year + 1),
        )
        self.theory2 = TheoryCourse.objects.create(
            instructor=self.instructor,
            start_date=date.today(),
        )

    def test_theorys_view(self):
        response = self.client.get("/home/theories/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Smith")
        self.assertNotContains(
            response,
            date.today().replace(year=date.today().year + 1).strftime("%d.%m.%Y"),
        )
        self.assertContains(response, date.today().strftime("%d.%m.%Y"))
