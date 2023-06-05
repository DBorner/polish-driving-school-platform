from django.test import TestCase
from datetime import date
from users.models import Instructor, Qualification
from course.models import Category
from users.utils import get_instructor_qualifications
from django.db.models.query import QuerySet


class GetInstructorQualificationTest(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            surname="Smith",
            name="John",
            birth_date=date(2000, 1, 1),
            phone_number="123456789",
            instructor_id="123456789",
        )
        self.category1 = Category.objects.create(
            symbol="A", price=100, required_practical_hours=10
        )
        self.category2 = Category.objects.create(
            symbol="B", price=100, required_practical_hours=10
        )
        self.qualification = Qualification.objects.create(
            instructor=self.instructor,
            category=self.category1,
            date_of_achievement=date(2020, 1, 1),
        )

    def test_get_instructor_qualification(self):
        qualifications = get_instructor_qualifications(self.instructor.id)
        self.assertIsInstance(qualifications, QuerySet)
        self.assertEqual(len(qualifications), 1)
        self.assertEqual(qualifications[0], self.qualification)

    def test_get_instructor_qualification_with_no_qualifications(self):
        qualifications = get_instructor_qualifications(2)
        self.assertEqual(qualifications, None)
