from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from users.models import Instructor, Student, Qualification, Employee
from course.models import Vehicle, Course, Category, TheoryCourse, PracticalLesson


class NewStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "surname",
            "name",
            "birth_date",
            "phone_number",
            "email",
        ]


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = [
            "surname",
            "name",
            "birth_date",
            "date_of_employment",
            "phone_number",
            "instructor_id",
        ]


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "surname",
            "name",
            "birth_date",
            "date_of_employment",
        ]


class EditStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "surname",
            "name",
            "birth_date",
            "phone_number",
            "email",
        ]


class NewPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ["new_password1", "new_password2"]


class EditPracticalLessonForm(forms.ModelForm):
    class Meta:
        model = PracticalLesson
        fields = [
            "date",
            "start_time",
            "num_of_hours",
            "num_of_km",
            "cost",
            "vehicle",
        ]


class CreatePracticalLessonForm(forms.ModelForm):
    class Meta:
        model = PracticalLesson
        fields = [
            "course",
            "date",
            "start_time",
            "num_of_hours",
            "num_of_km",
            "cost",
            "vehicle",
        ]


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "pkk_number",
            "cost",
            "category",
            "student",
            "instructor",
        ]


class EditCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "instructor",
            'status'
        ]


class NewTheoryForm(forms.ModelForm):
    class Meta:
        model = TheoryCourse
        fields = ["type", "start_date", "instructor"]


class TheoryEditForm(forms.ModelForm):
    class Meta:
        model = TheoryCourse
        fields = ["type", "start_date", "instructor"]


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "brand",
            "model",
            "year_of_production",
            "registration_number",
            "gearbox_type",
            "type",
        ]


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "symbol",
            "description",
            "required_practical_hours",
            "price",
            "is_discount",
            "discount_price",
            "photo",
        ]


class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "description",
            "required_practical_hours",
            "price",
            "is_discount",
            "discount_price",
            "photo",
        ]


class CreateQualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ["category", "date_of_achievement"]
