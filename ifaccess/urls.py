"""ifaccess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ifaccapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # daqui para baixo, deveria se utilizar o include, e todas essas linhas deveriam estar no arquivo ifaccapp/urls.py
    path('', views.home, name='home'),
    path('home.html', views.home, name='home'),
    path('people.html', views.people, name='people'),
    path('ambients.html', views.ambients, name='ambients'),
    path('schedules.html', views.schedules, name='schedules'),
    path('signup.html', views.signup, name='signup'),
    path('login.html', views.loginView, name='login'),
    path('logout.html', views.logoutView, name='logout'),
    path('register/register_ambient.html', views.register_ambient, name='register_ambient'),
    path('register/register_person.html', views.register_person, name='register_person'),
    path('register/register_schedule.html', views.register_schedule, name='register_schedule'),
    path('edit/<str:pk>/edit_ambient.html', views.edit_ambient, name='edit_ambient'),
    path('edit/<int:pk>/edit_person.html', views.edit_person, name='edit_person'),
    path('edit/<int:pk>/edit_schedule.html', views.edit_schedule, name='edit_schedule'),
    path('<int:pk>/people.html', views.remove_person, name='remove_person'),
    path('<str:pk>/ambients.html', views.remove_ambient, name='remove_ambient'),
    path('<int:pk>/schedules.html', views.remove_schedule, name='remove_schedule'),
    path('<str:pk>/specific_schedules.html', views.view_specific_schedules, name='view_specific_schedules'),
    path('administration.html', views.administration, name='administration'),
    path('csv_generator.html', views.csv_generator, name='csv_generator'),
]

