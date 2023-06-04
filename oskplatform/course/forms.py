from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from users.models import Instructor, Student, Qualification
from course.models import Vehicle, Course, Category, TheoryCourse


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


class EditPracticalLessonForm(forms.Form):
    date = forms.DateField(label="Data")
    start_time = forms.TimeField(label="Godzina rozpoczęcia")
    num_of_hours = forms.IntegerField(label="Liczba godzin", min_value=1, max_value=10)
    num_of_km = forms.IntegerField(
        label="Liczba kilometrów", required=False, min_value=0
    )
    cost = forms.DecimalField(
        max_digits=10, decimal_places=2, label="Koszt", required=False, min_value=0
    )
    instructor = forms.ModelChoiceField(
        queryset=Instructor.objects.all(), label="Instruktor"
    )
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.filter(is_available="True"),
        label="Pojazd",
        required=False,
    )


class CreatePracticalLessonForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Kurs")
    date = forms.DateField(label="Data")
    start_time = forms.TimeField(label="Godzina rozpoczęcia")
    num_of_hours = forms.IntegerField(label="Liczba godzin", min_value=1, max_value=10)
    num_of_km = forms.IntegerField(
        label="Liczba kilometrów", required=False, min_value=0
    )
    cost = forms.DecimalField(
        max_digits=10, decimal_places=2, label="Koszt", required=False, min_value=0
    )
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.filter(is_available="True"),
        label="Pojazd",
        required=False,
    )


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
