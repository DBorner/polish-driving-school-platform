from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from users.models import Instructor
from course.models import Vehicle


class NewStudentForm(forms.Form):
    surname = forms.CharField(max_length=50, min_length=3, label='Nazwisko')
    name = forms.CharField(max_length=50, min_length=3, label='Imię')
    birth_date = forms.DateField(label='Data urodzenia')
    phone_number = forms.CharField(max_length=20, label='Numer telefonu', required=False)
    email = forms.EmailField(max_length=50, label='Adres e-mail', required=False)
    

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']
        
        
class EditPracticalLessonForm(forms.Form):
    date = forms.DateField(label='Data')
    start_time = forms.TimeField(label='Godzina rozpoczęcia')
    num_of_hours = forms.IntegerField(label='Liczba godzin', min_value=1, max_value=10)
    num_of_km = forms.IntegerField(label='Liczba kilometrów', required=False, min_value=0)
    cost = forms.DecimalField(max_digits=10, decimal_places=2, label='Koszt', required=False, min_value=0)
    instructor = forms.ModelChoiceField(queryset=Instructor.objects.all(), label='Instruktor')
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all(), label='Pojazd', required=False)
    