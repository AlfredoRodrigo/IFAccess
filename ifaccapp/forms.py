from django import forms
from .models import Person
from .models import Ambient
from .models import Schedule
from .models import Signup
from .models import Login

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'registration', 'tag')

class AmbientForm(forms.ModelForm):
    class Meta:
        model = Ambient
        fields = ('type', 'name', 'ID', 'IP', 'mask')

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('day', 'entryTime', 'exitTime', 'person', 'ambient')

class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ('user', 'password', 'confirmPassword')
        widgets = {
            'password': forms.PasswordInput(),
            'confirmPassword': forms.PasswordInput(),
        }

class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ('user', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }