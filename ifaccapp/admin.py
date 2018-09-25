from django.contrib import admin
from .models import Person
from .models import Ambient
from .models import Schedule

# Register your models here.
admin.site.register(Person)
admin.site.register(Ambient)
admin.site.register(Schedule)
