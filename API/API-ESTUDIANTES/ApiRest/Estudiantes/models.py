from django.db import models

# Create your models here.
from django.db import models

class Estudiante(models.Model):
    IdEstudiante = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    Apellido = models.CharField(max_length=100)
    DNI = models.CharField(max_length=20)
    Direccion = models.CharField(max_length=200)
    Telefono = models.CharField(max_length=20)
    Correo = models.EmailField()

    def __str__(self):
        return self.Nombre
