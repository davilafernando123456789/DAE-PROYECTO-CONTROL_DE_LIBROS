from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Prestamo,Libro,Estudiante,Encargado
# Create your views de inicio de sesion.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            prestamos_listado = Prestamo.objects.all()
            encargados_listado = Encargado.objects.all()
            libros_listado = Libro.objects.all()
            estudiantes_listado = Estudiante.objects.all()
            return render(request, 'Gestion_prestamo.html', {"prestamos":prestamos_listado,"encargados": encargados_listado,"libros":libros_listado,"estudiantes":estudiantes_listado})  # Reemplaza 'nombre_de_la_pagina' con el nombre de la página a la que deseas redirigir
        else:
            # El usuario no ha proporcionado credenciales válidas
            pass
    return render(request,'login.html')

def home(request):
    prestamos=Prestamo.objects.all()
    encargados = Encargado.objects.all()
    libros = Libro.objects.all()
    estudiantes = Estudiante.objects.all()

    return render(request, 'Gestion_prestamo.html',{'prestamos':prestamos,'encargados': encargados,'libros': libros,'estudiantes': estudiantes,})

def prestamo_form(request):
    if request.method == 'POST':
        Id_Encargado = request.POST["encargado"]
        Id_Libro = request.POST["libro"]
        Id_Estudiante = request.POST["estudiante"]
        FechaPrestamo = request.POST["fecha_prestamo"]
        FechaDevolucion = request.POST["fecha_devolucion"]

        encargado=Encargado.objects.get(IdEncargado=Id_Encargado)
        libro=Libro.objects.get(IdLibro=Id_Libro)
        estudiante=Estudiante.objects.get(IdEstudiante=Id_Estudiante)
        # Crear el registro de préstamo
        prestamo = Prestamo.objects.create(IdEncargado=encargado,IdLibro=libro,IdEstudiante=estudiante,FechaPrestamo=FechaPrestamo,FechaDevolucion=FechaDevolucion)
        return redirect('/home')
    
def eliminarprestamo(request, IdPrestamo):
    prestamo= Prestamo.objects.get(IdPrestamo=IdPrestamo)
    prestamo.delete()
    return redirect('/home')

def editar_prestamo(request, IdPrestamo):
    prestamo = Prestamo.objects.get(IdPrestamo=IdPrestamo)

    if request.method == 'POST':
        Id_Encargado = request.POST["encargado"]
        Id_Libro = request.POST["libro"]
        Id_Estudiante = request.POST["estudiante"]
        FechaPrestamo = request.POST["fecha_prestamo"]
        FechaDevolucion = request.POST["fecha_devolucion"]

        encargado = Encargado.objects.get(IdEncargado=Id_Encargado)
        libro = Libro.objects.get(IdLibro=Id_Libro)
        estudiante = Estudiante.objects.get(IdEstudiante=Id_Estudiante)

        # Actualizar los campos del registro de préstamo existente
        prestamo.IdEncargado = encargado
        prestamo.IdLibro = libro
        prestamo.IdEstudiante = estudiante
        prestamo.FechaPrestamo = FechaPrestamo
        prestamo.FechaDevolucion = FechaDevolucion
        prestamo.save()
        return redirect('/home')
    # Si la solicitud es GET, renderizar el formulario de edición con los datos actuales del préstamo
    encargados = Encargado.objects.all()
    libros = Libro.objects.all()
    estudiantes = Estudiante.objects.all()

    context = {'prestamo': prestamo,'encargados': encargados,'libros': libros,'estudiantes': estudiantes,}

    return render(request, 'Editar_Prestamo.html', context)
