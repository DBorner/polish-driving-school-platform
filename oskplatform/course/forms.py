from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model


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