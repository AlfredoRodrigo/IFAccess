from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .models import Ambient
from .models import Person
from .models import Schedule
from .forms import PersonForm
from .forms import AmbientForm
from .forms import ScheduleForm

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
    if request.method == "POST":
        register_ambient = AmbientForm(request.POST)
        if register_ambient.is_valid():
            ambient = register_ambient.save()
            ambient.save()
            return redirect('ambients')
    else:
        register_ambient = AmbientForm()
    return render(request, 'ifaccapp/register/register_ambient.html', {'register_ambient': register_ambient})

def register_person(request):
    if request.method == "POST":
        register_person = PersonForm(request.POST)
        if register_person.is_valid():
            person = register_person.save()
            person.save()
            return redirect('people')
    else:
        register_person = PersonForm()
    return render(request, 'ifaccapp/register/register_person.html', {'register_person': register_person})

def register_schedule(request):
    if request.method == "POST":
        register_schedule = ScheduleForm(request.POST)
        if register_schedule.is_valid():
            schedule = register_schedule.save()
            schedule.save()
            return redirect('schedules')
    else:
        register_schedule = ScheduleForm()
    return render(request, 'ifaccapp/register/register_schedule.html', {'register_schedule': register_schedule})

def edit_ambient(request, pk):
    ambient = get_object_or_404(Ambient, pk=pk)
    if request.method == "POST":
        edit_ambient = AmbientForm(request.POST, instance=ambient)
        if edit_ambient.is_valid():
            ambient = edit_ambient.save()
            ambient.save()
            return redirect('ambients')
    else:
        edit_ambient = AmbientForm(instance=ambient)
    return render(request, 'ifaccapp/edit/edit_ambient.html', {'edit_ambient': edit_ambient})

def edit_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == "POST":
        edit_person = PersonForm(request.POST, instance=person)
        if edit_person.is_valid():
            person = edit_person.save()
            person.save()
            return redirect('people')
    else:
        edit_person = PersonForm(instance=person)
    return render(request, 'ifaccapp/edit/edit_person.html', {'edit_person': edit_person})

def edit_schedule(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == "POST":
        edit_schedule = ScheduleForm(request.POST, instance=schedule)
        if edit_schedule.is_valid():
            schedule = edit_schedule.save()
            schedule.save()
            return redirect('schedules')
    else:
        edit_schedule = ScheduleForm(instance=schedule)
    return render(request, 'ifaccapp/edit/edit_schedule.html', {'edit_schedule': edit_schedule})

def remove_person(request, pk):
    Person.objects.get(pk=pk).delete()
    return redirect('people')

def remove_ambient(request, pk):
    Ambient.objects.get(pk=pk).delete()
    return redirect('ambients')

def remove_schedule(request, pk):
    Schedule.objects.get(pk=pk).delete()
    return redirect('schedules')