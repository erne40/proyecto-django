from django.db import models

# Create your models here.

class Animal(models.Model):
    nombre = models.CharField(max_length=20)
    edad = models.IntegerField()
    
    def __str__(self):
        return f'Soy {self.nombre}, tengo {self.edad}'

class Persona(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()