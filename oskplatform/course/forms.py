from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from users.models import Instructor, Student, Qualification, Employee
from course.models import Vehicle, Course, Category, TheoryCourse, PracticalLesson


class NewStudentForm(forms.Form):
    surname = forms.CharField(max_length=50, min_length=3, label="Nazwisko")
    name = forms.CharField(max_length=50, min_length=3, label="Imię")
    birth_date = forms.DateField(label="Data urodzenia")
    phone_number = forms.CharField(
        max_length=20, label="Numer telefonu", required=False
    )
    email = forms.EmailField(max_length=50, label="Adres e-mail", required=False)


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


class EditStudentForm(forms.Form):
    surname = forms.CharField(max_length=50, min_length=3, label="Nazwisko")
    name = forms.CharField(max_length=50, min_length=3, label="Imię")
    birth_date = forms.DateField(label="Data urodzenia")
    phone_number = forms.CharField(
        max_length=20, label="Numer telefonu", required=False
    )
    email = forms.EmailField(max_length=50, label="Adres e-mail", required=False)


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


class CreateCourseForm(forms.Form):
    pkk_number = forms.CharField(max_length=20, min_length=20, label="Numer PKK")
    cost = forms.DecimalField(max_digits=10, decimal_places=2, label="Koszt")
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_available="True"), label="Kategoria"
    )
    student = forms.ModelChoiceField(queryset=Student.objects.all(), label="Kursant")
    instructor = forms.ModelChoiceField(
        queryset=Instructor.objects.filter(is_active="True"),
        label="Instruktor",
        required=False,
    )


class EditCourseForm(forms.Form):
    instructor = forms.ModelChoiceField(
        queryset=Instructor.objects.filter(is_active="True"),
        label="Instruktor",
        required=False,
    )
    course_status_choices = [
        ("R", "Rozpoczęty"),
        ("Z", "Zakończony"),
        ("A", "Anulowany"),
    ]
    status = forms.ChoiceField(choices=course_status_choices, label="Status kursu")


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
