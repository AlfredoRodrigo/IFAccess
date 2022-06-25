from django.core.exceptions import ValidationError
from django.db import models

class Person(models.Model):
    name = models.CharField(null=True, max_length=100, verbose_name="Nome")
    registration = models.BigIntegerField(primary_key=True, verbose_name="Matrícula")  # matrícula
    tag = models.CharField(null=True, max_length=100, verbose_name="Tag RFID")

    def __str__(self):
        return self.name

class Ambient(models.Model):
    # Constantes para os tipos de locais
    COORDENACAO = "Coordenação"
    SALA = "Sala"
    LABORATORIO = "Laboratório"

    # Possíveis escolhas para os tipos de locais
    TYPE_CHOICES = (
        (COORDENACAO, 'Coordenação'),
        (SALA, 'Sala'),
        (LABORATORIO, 'Laboratório'),
    )

    type = models.TextField(null=True, max_length=50, choices=TYPE_CHOICES, verbose_name="Tipo de ambiente")
    name = models.CharField(null=True, max_length=100, verbose_name="Nome")
    ID = models.CharField(primary_key=True, max_length=50)
    IP = models.CharField(null=True, max_length=15, verbose_name="IP")
    mask = models.CharField(null=True, max_length=15, verbose_name="Máscara")


    def __str__(self):
        return self.name


class Schedule(models.Model):
    # Constantes para os dias
    DOMINGO = 'Domingo'
    SEGUNDA = 'Segunda-feira'
    TERCA = 'Terça-feira'
    QUARTA = 'Quarta-feira'
    QUINTA = 'Quinta-feira'
    SEXTA = 'Sexta-feira'
    SABADO = 'Sábado'

    # Possíveis escolhas para os dias
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

    def clean(self):
        if self.entryTime > self.exitTime:
            raise ValidationError('O horário de entrada é maior que o horário de saída.')

class Signup(models.Model):
    user = models.CharField(null=True, max_length=50, verbose_name="Usuário")
    password = models.CharField(null=True, max_length=50, verbose_name="Senha")
    confirmPassword = models.CharField(null=True, max_length=50, verbose_name="Confirmação de senha")

class Login(models.Model):
    user = models.CharField(null=True, max_length=50, verbose_name="Usuário")
    password = models.CharField(null=True, max_length=50, verbose_name="Senha")