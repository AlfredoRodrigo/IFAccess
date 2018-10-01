from django import forms
from .models import Person
from .models import Ambient
from .models import Schedule

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'registration', 'tag')

class AmbientForm(forms.ModelForm):
    class Meta:
        model = Ambient
        fields = ('type', 'name', 'ID')

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('day', 'entryTime', 'exitTime', 'person', 'ambient')