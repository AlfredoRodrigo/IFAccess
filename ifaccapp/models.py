from django.db import models

class Person(models.Model):
    name = models.TextField(null=True, max_length=100, verbose_name="Nome")
    registration = models.BigIntegerField(primary_key=True, verbose_name="Matrícula")  # matrícula
    tag = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Ambient(models.Model):
    name = models.TextField(null=True, max_length=100, verbose_name="Nome")
    ID = models.TextField(primary_key=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    DOMINGO = 'Domingo'
    SEGUNDA = 'Segunda-feira'
    TERCA = 'Terça-feira'
    QUARTA = 'Quarta-feira'
    QUINTA = 'Quinta-feira'
    SEXTA = 'Sexta-feira'
    SABADO = 'Sábado'

    DAY_CHOICES = (
        (DOMINGO, 'Domingo'),
        (SEGUNDA, 'Segunda-feira'),
        (TERCA, 'Terça-feira'),
        (QUARTA, 'Quarta-feira'),
        (QUINTA, 'Quinta-feira'),
        (SEXTA, 'Sexta-feira'),
        (SABADO, 'Sábado'),
    )

    day = models.TextField(null=True, max_length=50, choices=DAY_CHOICES, verbose_name="Dia")
    entryTime = models.TimeField(null=True, verbose_name="Hora de entrada")
    exitTime = models.TimeField(null=True, verbose_name="Hora de saída")
    person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name="Pessoa")
    ambient = models.ForeignKey('Ambient', on_delete=models.CASCADE, verbose_name="Ambiente")