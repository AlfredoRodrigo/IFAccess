from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Ambient
from .models import Person
from .models import Schedule
from .forms import PersonForm
from .forms import AmbientForm
from .forms import ScheduleForm
from .forms import SignupForm
from .forms import LoginForm
import csv
import random
import time

from paho.mqtt import client as mqtt_client

broker = 'mqtt.eclipseprojects.io'
port = 1883
topic = "IFAccess"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

# Create your views here.

@login_required(redirect_field_name = None, login_url='/login.html')
def home(request):
    return render(request, 'ifaccapp/home.html', {'home': home})

@login_required(redirect_field_name = None, login_url='/login.html')
def people(request):
    people = Person.objects.all()
    return render(request, 'ifaccapp/people.html', {'people': people})

@login_required(redirect_field_name = None, login_url='/login.html')
def ambients(request):
    ambients = Ambient.objects.all()
    return render(request, 'ifaccapp/ambients.html', {'ambients': ambients})

@login_required(redirect_field_name = None, login_url='/login.html')
def schedules(request):
    schedules = Schedule.objects.all()
    return render(request, 'ifaccapp/schedules.html', {'schedules': schedules})

@login_required(redirect_field_name = None, login_url='/login.html')
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

@login_required(redirect_field_name = None, login_url='/login.html')
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

@login_required(redirect_field_name = None, login_url='/login.html')
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

@login_required(redirect_field_name = None, login_url='/login.html')
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

@login_required(redirect_field_name = None, login_url='/login.html')
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

@login_required(redirect_field_name = None, login_url='/login.html')
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

@login_required(redirect_field_name = None, login_url='/login.html')
def remove_person(request, pk):
    Person.objects.get(pk=pk).delete()
    return redirect('people')

@login_required(redirect_field_name = None, login_url='/login.html')
def remove_ambient(request, pk):
    Ambient.objects.get(pk=pk).delete()
    return redirect('ambients')

@login_required(redirect_field_name = None, login_url='/login.html')
def remove_schedule(request, pk):
    Schedule.objects.get(pk=pk).delete()
    return redirect('schedules')

@login_required(redirect_field_name = None, login_url='/login.html')
def view_specific_schedules(request, pk):
    schedules = Schedule.objects.filter(ambient=pk)
    return render(request, 'ifaccapp/specific_schedules.html', {'schedules': schedules})

@login_required(redirect_field_name = None, login_url='/login.html')
def administration(request):
    return render(request, 'ifaccapp/administration.html')

@login_required(redirect_field_name = None, login_url='/login.html')
def csv_generator(request):

    schedules = Schedule.objects.all()
    rows = []

    with open('cadastro.csv', 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)

        for schedule in schedules:
            row = []
            row.append(schedule.day)
            row.append(str(schedule.entryTime))
            row.append(str(schedule.exitTime))
            row.append(str(schedule.person.registration))
            row.append(schedule.ambient.ID)
            row.append(str(schedule.person.rfidtag) + ";")
            rows.append(row)

        for r in rows:
            print(r)
            writer.writerow(r)

    '''
    writer = csv.writer(open("cadastro.csv", "w"))

    for schedule in schedules:
        row = []
        row.append(schedule.day)
        row.append(str(schedule.entryTime))
        row.append(str(schedule.exitTime))
        row.append(str(schedule.person.registration))
        row.append(schedule.ambient.ID)
        row.append(schedule.person.tag)
        rows.append(row)

    for r in rows:
        writer.writerow(r)
        
    '''
    '''
    with open('cadastro.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")

        for row in spamreader:
            print("".join(row))
    '''

    sent_to_arduino()

    return redirect('administration')

#@login_required(redirect_field_name = None, login_url='/login.html')
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao broker MQTT!")
        else:
            print("A conexão com o broker MQTT falhou. Código de retorno: %d\n", rc)

    #setando a conexão do ID do cliente
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

#@login_required(redirect_field_name = None, login_url='/login.html')
def publish(client):
    with open('cadastro.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")

        client.publish(topic, "BEGIN")

        for row in spamreader:
            time.sleep(1/10)
            client.publish(topic, ",".join(row))

        client.publish(topic, "END")

    '''
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Mensagem '{msg}' enviada ao tópico `{topic}`")
        else:
            print(f"Falha ao enviar a mensagem ao tópico `{topic}`")
        msg_count += 1
    '''

#@login_required(redirect_field_name = None, login_url='/login.html')
def sent_to_arduino():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()
    
#@login_required(redirect_field_name = None, login_url='/login.html')
def signup(request):
    signup = SignupForm()
    if request.method == "POST":
        signup = SignupForm(data=request.POST)

        if signup.is_valid():
            username = signup.cleaned_data.get('user')
            password = signup.cleaned_data.get('password')
            confirmPassword = signup.cleaned_data.get('confirmPassword')

            if username and password and confirmPassword and (password == confirmPassword):
                userObject = User.objects.create_user(
                    username = username,
                    password = password
                )

                if userObject:
                    return HttpResponseRedirect(reverse('login'))

    return render(request, 'ifaccapp/signup.html', {'signup': signup, 'error': "Usuário ou senha inválidos."})

def loginView(request):
    loginForm = LoginForm()

    if request.method == "GET":
        return render(request, 'ifaccapp/login.html', {'login': loginForm})

    if request.method == "POST":
        loginForm = LoginForm(data=request.POST)

        if loginForm.is_valid():
            username = loginForm.cleaned_data.get('user')
            password = loginForm.cleaned_data.get('password')

            if username and password and authenticate(username=username, password=password):
                user = User.objects.get_by_natural_key(username)
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

        return render(request, 'ifaccapp/login.html', {'login': loginForm, 'error': "Usuário ou senha inválidos."})

@login_required(redirect_field_name = None, login_url='/login.html')
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))