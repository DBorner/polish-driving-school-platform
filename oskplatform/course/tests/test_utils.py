from django.test import TestCase
from datetime import date
from users.models import Student, Instructor, Qualification, CustomUser
from course.models import Category, Vehicle, Course, TheoryCourse, PracticalLesson
from datetime import datetime
from model_bakery import baker
from course.utils import (
    check_instructor_qualifications,
    get_course_dates,
    is_student_active,
    requires_permissions,
    generate_password,
    check_start_date_for_theory_course,
)


class CheckInstructorQualificationsTest(TestCase):
    def setUp(self):
        self.instructor = baker.make(Instructor)
        self.category = baker.make(Category, required_practical_hours=10)
        self.category2 = baker.make(Category, required_practical_hours=10)
        self.category3 = baker.make(Category, required_practical_hours=10)
        self.qualification = baker.make(
            Qualification,
            instructor=self.instructor,
            category=self.category,
            date_of_achievement=datetime(2020, 1, 1),
        )
        self.qualification2 = baker.make(
            Qualification,
            instructor=self.instructor,
            category=self.category2,
            date_of_achievement=datetime(2020, 1, 1),
        )

    def test_check_instructor_qualifications_with_no_category(self):
        self.assertTrue(check_instructor_qualifications(self.instructor, None))

    def test_check_instructor_qualifications_with_no_instructor(self):
        self.assertTrue(check_instructor_qualifications(None, self.category))

    def test_check_instructor_qualifications_with_no_qualifications(self):
        self.assertFalse(
            check_instructor_qualifications(self.instructor, self.category3)
        )

    def test_check_instructor_qualifications_with_qualifications(self):
        self.assertTrue(check_instructor_qualifications(self.instructor, self.category))
        self.assertTrue(
            check_instructor_qualifications(self.instructor, self.category2)
        )


class GetCourseDatesTest(TestCase):
    def _get_first_weekday(self, weekday):
        date = datetime.today()
        for _ in range(0, 7):
            date = date.replace(day=date.day + 1)
            if date.weekday() == weekday:
                return date
        return None

    def setUp(self):
        self.instructor = baker.make(Instructor)
        self.theory = baker.make(
            TheoryCourse,
            instructor=self.instructor,
            start_date=self._get_first_weekday(0),
        )
        self.theory2 = baker.make(
            TheoryCourse,
            instructor=self.instructor,
            start_date=self._get_first_weekday(5),
            type="W",
        )

    def test_get_course_dates_with_no_category(self):
        self.assertEqual(get_course_dates(None), None)

    def test_t_type_get_course_dates(self):
        self.assertEqual(len(get_course_dates(self.theory.id)), 5)

    def test_w_type_get_course_dates(self):
        self.assertEqual(len(get_course_dates(self.theory2.id)), 4)

    def test_wrong_type_get_course_dates(self):
        theory3 = baker.make(
            TheoryCourse,
            instructor=self.instructor,
            start_date=self._get_first_weekday(3),
            type="W",
        )
        theory4 = baker.make(
            TheoryCourse,
            instructor=self.instructor,
            start_date=self._get_first_weekday(3),
            type="T",
        )
        self.assertEqual(get_course_dates(theory3.id), None)
        self.assertEqual(get_course_dates(theory4.id), None)


class IsStudentActiveTest(TestCase):
    def setUp(self):
        self.student = baker.make(Student)
        self.student2 = baker.make(Student)
        self.category = baker.make(Category, required_practical_hours=10)
        self.course = baker.make(Course, category=self.category, student=self.student)

    def test_is_student_active_with_active_student(self):
        self.assertTrue(is_student_active(self.student))

    def test_is_student_active_with_inactive_student(self):
        self.assertFalse(is_student_active(self.student2))

    def test_is_student_active_with_no_student(self):
        self.assertFalse(is_student_active(None))


class RequiresPermissionsTest(TestCase):
    def setUp(self):
        self.user_i = baker.make(CustomUser, permissions_type="I")
        self.user_s = baker.make(CustomUser, permissions_type="S")
        self.user_a = baker.make(CustomUser, permissions_type="A")
        self.user_e = baker.make(CustomUser, permissions_type="E")

    def test_requires_permissions_with_instructor(self):
        self.assertTrue(requires_permissions(self.user_i, "I"))
        self.assertNotEqual(requires_permissions(self.user_i, "S"), True)

    def test_requires_permissions_with_student(self):
        self.assertTrue(requires_permissions(self.user_s, "S"))
        self.assertNotEqual(requires_permissions(self.user_s, "I"), True)

    def test_requires_permissions_with_admin(self):
        self.assertTrue(requires_permissions(self.user_a, "A"))
        self.assertNotEqual(requires_permissions(self.user_a, "I"), True)

    def test_requires_permissions_with_employee(self):
        self.assertTrue(requires_permissions(self.user_e, "E"))
        self.assertNotEqual(requires_permissions(self.user_e, "I"), True)

    def test_requires_permissions_with_no_user(self):
        self.assertNotEqual(requires_permissions(None, "I"), True)


class GeneratePasswordTest(TestCase):
    def test_generate_password(self):
        self.assertEqual(len(generate_password()), 6)
        self.assertNotEqual(generate_password(), generate_password())


class CheckStartDateForTheoryCourseTest(TestCase):
    def _get_first_weekday(self, weekday):
        date = datetime.today()
        for _ in range(0, 7):
            date = date.replace(day=date.day + 1)
            if date.weekday() == weekday:
                return date
        return None

    def setUp(self):
        self.instructor = baker.make(Instructor)
        self.theory = baker.make(
            TheoryCourse,
            instructor=self.instructor,
            start_date=self._get_first_weekday(0),
        )
        self.theory2 = baker.make(
            TheoryCourse,
            instructor=self.instructor,
            start_date=self._get_first_weekday(5),
            type="W",
        )
        self.theory3 = baker.make(
            TheoryCourse,
            instructor=self.instructor,
            start_date=self._get_first_weekday(3),
            type="W",
        )
        self.theory4 = baker.make(
            TheoryCourse,
            instructor=self.instructor,
            start_date=self._get_first_weekday(3),
            type="T",
        )

    def test_check_start_date_for_theory_course_with_no_course(self):
        self.assertFalse(check_start_date_for_theory_course(None, None))

    def test_check_start_date_for_theory_course_with_course(self):
        self.assertTrue(check_start_date_for_theory_course(self.theory.start_date, self.theory.type))
        self.assertTrue(check_start_date_for_theory_course(self.theory2.start_date, self.theory2.type))
        self.assertFalse(check_start_date_for_theory_course(self.theory3.start_date, self.theory3.type))
        self.assertFalse(check_start_date_for_theory_course(self.theory4.start_date, self.theory4.type))
