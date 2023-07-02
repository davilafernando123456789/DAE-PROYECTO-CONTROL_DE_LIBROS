from django.db import models
from datetime import datetime, timedelta
# Create your models here.
class Categoria(models.Model):
    Idcategoria = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.Nombre


class Editorial(models.Model):
    idEditorial = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    Telefono = models.CharField(max_length=20)
    Correo = models.EmailField()
    Pais = models.CharField(max_length=50)
    Ciudad = models.CharField(max_length=50)
    Direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.Nombre


class Autor(models.Model):
    IdAutor = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    Genero = models.CharField(max_length=100)
    Apellido = models.CharField(max_length=100)
    Fecha_nacimiento = models.DateField()
    Nacionalidad = models.CharField(max_length=50)

    def __str__(self):
        return self.Nombre


class Libro(models.Model):
    IdLibro = models.AutoField(primary_key=True)
    Titulo = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=20)
    Autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    Editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    Categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    Año_publicacion = models.PositiveIntegerField()
    Disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return self.Titulo


class Prestamo(models.Model):
    IdPrestamo = models.AutoField(primary_key=True)
    IdEncargado = models.ForeignKey('Encargado', on_delete=models.CASCADE)
    IdLibro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    IdEstudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE)
    FechaPrestamo = models.DateField()
    FechaDevolucion = models.DateField()

    def __str__(self):
        return f"Prestamo {self.IdPrestamo}"


class Devolucion(models.Model):
    IdDevolucion = models.AutoField(primary_key=True)
    IdPrestamo = models.OneToOneField(Prestamo, on_delete=models.CASCADE)
    Fecha_entrega = models.DateField()
    Estado = models.CharField(max_length=50)

    def __str__(self):
        return f"Devolucion {self.IdDevolucion}"


class Penalizacion(models.Model):
    IdPenalizacion = models.AutoField(primary_key=True)
    IdEstudiante = models.OneToOneField('Estudiante', on_delete=models.CASCADE)
    Falseecha_inicio = models.DateField()
    Fecha_final = models.DateField()
    Estado = models.CharField(max_length=50)

    def __str__(self):
        return f"Penalizacion {self.IdPenalizacion}"


    @property
    def calcular_estado(self):
        fecha_actual = datetime.now().date()

        if fecha_actual > self.Fecha_final:
            self.Estado = 'Moroso'
        else:
            self.Estado = 'Apto'

        return self.Estado
    
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


class Encargado(models.Model):
    IdEncargado = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    Apellido = models.CharField(max_length=100)
    Direccion = models.CharField(max_length=200)
    Telefono = models.CharField(max_length=20)
    Correo = models.EmailField()
    IdCredenciales = models.OneToOneField('Credenciales', on_delete=models.CASCADE)

    def __str__(self):
        return self.Nombre


class Credenciales(models.Model):
    IdCredenciales = models.AutoField(primary_key=True)
    Usuario = models.CharField(max_length=50)
    Contraseña = models.CharField(max_length=50)

    def __str__(self):
        return self.Usuario