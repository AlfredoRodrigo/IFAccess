from django.db import models


class Person(models.Model):
    name = models.TextField(null=True)
    registration = models.BigIntegerField(primary_key=True)  # matrícula
    tag = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Ambient(models.Model):
    name = models.TextField(null=True)
    ID = models.TextField(primary_key=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    day = models.DateField(null=True)
    entryTime = models.TimeField(null=True)
    exitTime = models.TimeField(null=True)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    ambient = models.ForeignKey('Ambient', on_delete=models.CASCADE)