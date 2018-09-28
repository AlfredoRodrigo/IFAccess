from django.shortcuts import render
from .models import Ambient
from .models import Person
from .models import Schedule

# Create your views here.


def home(request):
    return render(request, 'ifaccapp/home.html', {'home': home})

def people(request):
    people = Person.objects.all()
    return render(request, 'ifaccapp/people.html', {'people': people})

def ambients(request):
    ambients = Ambient.objects.all()
    return render(request, 'ifaccapp/ambients.html', {'ambients': ambients})

def schedules(request):
    schedules = Schedule.objects.all()
    return render(request, 'ifaccapp/schedules.html', {'schedules': schedules})

def register_ambient(request):
    return render(request, 'ifaccapp/register/register_ambient.html', {'register_ambient': register_ambient})

def register_person(request):
    return render(request, 'ifaccapp/register/register_person.html', {'register_person': register_person})

def register_schedule(request):
    return render(request, 'ifaccapp/register/register_schedule.html', {'register_schedule': register_schedule})