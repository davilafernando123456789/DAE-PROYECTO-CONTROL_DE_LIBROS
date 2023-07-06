from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from .models import Prestamo,Libro,Estudiante,Encargado, Penalizacion, Devolucion, Credenciales
from django.db.models import Q
from django.http import JsonResponse
import requests
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.db import connection
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            credenciales = Credenciales.objects.get(Usuario=username, Contraseña=password)
            encargado = Encargado.objects.get(IdEncargado=credenciales.IdEncargado_id)

            request.session['IdEncargado'] = encargado.IdEncargado
            request.session['NombreEncargado'] = encargado.Nombre

            return redirect('/home')  # Reemplaza '/home' con la URL o ruta a la página principal luego del inicio de sesión
        except Credenciales.DoesNotExist:
            messages.error(request, 'Credenciales inválidas')
            return redirect('/')  # Reemplaza '/' con la URL o ruta a la página de inicio de sesión

    return render(request, 'login.html')

def prestamos_vencidos(request):
    prestamos = Prestamo.objects.filter(devolucion__Estado='No entregado')
    libros = Libro.objects.all()
    estudiantes = Estudiante.objects.all()
    actualizar_penalizacion(request)
    context = {'prestamos': prestamos,
                'libros': libros,
                'estudiantes': estudiantes,
               }
    return render(request, 'prestamos_vencidos.html', context)

def home(request):
    prestamos = Prestamo.objects.all()
    encargados = Encargado.objects.all()
    libros = Libro.objects.all()
    estudiantes = Estudiante.objects.all()
    penalizaciones = Penalizacion.objects.all()
    
    actualizar_penalizacion(request)
    return render(request, 'Gestion_prestamo.html', {
        'prestamos': prestamos,
        'encargados': encargados,
        'libros': libros,
        'estudiantes': estudiantes,
        'penalizaciones': penalizaciones,
        
    })

def listarEntrega(request):
    prestamos = Prestamo.objects.all()
    encargados = Encargado.objects.all()
    libros = Libro.objects.all()
    estudiantes = Estudiante.objects.all()
    penalizaciones = Penalizacion.objects.all()
    devoluciones = Devolucion.objects.all()
    actualizar_penalizacion(request)
    # Obtener el parámetro de búsqueda si está presente en la solicitud GET
    nombre_estudiante = request.GET.get('nombre_estudiante')

    # Filtrar los prestamos por nombre de estudiante si se proporciona el parámetro de búsqueda
    if nombre_estudiante:
        prestamos = prestamos.filter(IdEstudiante__Nombre__icontains=nombre_estudiante)
        devoluciones = devoluciones.filter(IdPrestamo__IdEstudiante__Nombre__icontains=nombre_estudiante)
    else:
        devoluciones = Devolucion.objects.all()

    context = {
        'prestamos': prestamos,
        'encargados': encargados,
        'libros': libros,
        'estudiantes': estudiantes,
        'penalizaciones': penalizaciones,
        'devoluciones': devoluciones,
    }
    return render(request, 'Gestion_entregas.html', context)

def listar_editar_penalizacion(request):
    penalizaciones = Penalizacion.objects.all()
    estudiantes = Estudiante.objects.all()
    if request.method == 'POST':
        penalizacion_id = request.POST.get('penalizacion_id')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_final = request.POST.get('fecha_final')
        estado = request.POST.get('estado')

        penalizacion = get_object_or_404(Penalizacion, pk=penalizacion_id)
        penalizacion.Falseecha_inicio = fecha_inicio
        penalizacion.Fecha_final = fecha_final
        penalizacion.Estado = estado
        penalizacion.save()

        return redirect('listar_editar_penalizacion')

    context = {
        'estudiantes': estudiantes,
        'penalizaciones': penalizaciones,
    }
    return render(request, 'listar_editar_penalizacion.html', context)

def listar_penalizacion(request):
    penalizaciones = Penalizacion.objects.all()
    estudiantes = Estudiante.objects.all()

    context = {
        'estudiantes': estudiantes,
        'penalizaciones': penalizaciones,
    }
    return render(request, 'Penalizaciones_activas.html', context)


import requests

def prestamo_form(request):
    # Obtener el parámetro de búsqueda si está presente en la solicitud GET
    query = request.GET.get('query')

    if request.method == 'POST':
        Id_Encargado = request.POST["encargado"]
        Id_Libro = request.POST["libro"]
        Id_Estudiante = request.POST["estudiante"]
        FechaPrestamo = request.POST["fecha_prestamo"]
        FechaDevolucion = request.POST["fecha_devolucion"]

        encargado = Encargado.objects.get(IdEncargado=Id_Encargado)
        libro = Libro.objects.get(IdLibro=Id_Libro)
        actualizar_penalizacion(request)

        # Obtener los datos del estudiante de la API
        url = 'http://127.0.0.1:8080/estudiantes/' + Id_Estudiante
        response = requests.get(url)
        estudiante_data = response.json()

        # Crear o actualizar el registro del estudiante
        estudiante, created = Estudiante.objects.update_or_create(
            IdEstudiante=Id_Estudiante,
            defaults={
                'Nombre': estudiante_data['Nombre'],
                'Apellido': estudiante_data['Apellido'],
                'DNI': estudiante_data['DNI'],
                'Direccion': estudiante_data['Direccion'],
                'Telefono': estudiante_data['Telefono'],
                'Correo': estudiante_data['Correo']
            }
        )

        prestamo = Prestamo.objects.create(IdEncargado=encargado, IdLibro=libro, IdEstudiante=estudiante,
                                           FechaPrestamo=FechaPrestamo, FechaDevolucion=FechaDevolucion)

        libro.Cantidad -= 1
        libro.save()

        devolucion = Devolucion.objects.create(IdPrestamo=prestamo, Fecha_entrega=None, Estado="No entregado")

        # Llamar a la función insertar_estudiante_en_penalizacion pasando el ID del estudiante
        return redirect('/home')

    prestamos = Prestamo.objects.all()

    # Filtrar los préstamos por nombre de estudiante o título de libro si se proporciona el parámetro de búsqueda
    if query:
        prestamos = prestamos.filter(Q(IdEstudiante__Nombre__icontains=query) | Q(IdLibro__Titulo__icontains=query))
    else:
        prestamos = prestamos.all()

    prestamo = Prestamo.objects.all()
    encargados = Encargado.objects.all()
    libros = Libro.objects.all()
    penalizaciones = Penalizacion.objects.all()

    url = 'http://127.0.0.1:8080/estudiantes/'
    response = requests.get(url)
    estudiantes = response.json()

    context = {'prestamo': prestamo, 'encargados': encargados, 'libros': libros, 'estudiantes': estudiantes,
                'penalizaciones': penalizaciones}

    return render(request, 'Gestion_prestamo.html', context)


def listarPrestamos(request):
    prestamos = Prestamo.objects.all()
    encargados = Encargado.objects.all()
    libros = Libro.objects.all()
    estudiantes = Estudiante.objects.all()
    penalizaciones = Penalizacion.objects.all()
    actualizar_penalizacion(request)
    context = {
        'prestamos': prestamos,
        'encargados': encargados,
        'libros': libros,
        'estudiantes': estudiantes,
        'penalizaciones': penalizaciones,
    }

    return render(request, 'Gestion_prestamo.html', context)


def lista_prestamos(request):
    prestamos = Prestamo.objects.all()
    encargados = Encargado.objects.all()
    libros = Libro.objects.all()
    estudiantes = Estudiante.objects.all()
    penalizaciones = Penalizacion.objects.all()

    # Obtener parámetros de búsqueda (si están presentes)
    tipo_consulta = request.GET.get('tipo_consulta')
    fecha = request.GET.get('fecha')

    # Realizar el filtrado de acuerdo a los parámetros de búsqueda
    if tipo_consulta == 'dia':
        fecha_actual = datetime.now().date()
        prestamos = prestamos.filter(FechaPrestamo=fecha_actual)
    elif tipo_consulta == 'semana':
        fecha_actual = datetime.now().date()
        fecha_inicio = fecha_actual - timedelta(days=7)
        prestamos = prestamos.filter(FechaPrestamo__gte=fecha_inicio, FechaPrestamo__lte=fecha_actual)
    elif tipo_consulta == 'mes':
        fecha_actual = datetime.now().date()
        fecha_inicio = fecha_actual - timedelta(days=30)
        prestamos = prestamos.filter(FechaPrestamo__gte=fecha_inicio, FechaPrestamo__lte=fecha_actual)
    elif tipo_consulta == 'personalizado' and fecha:
        fecha_seleccionada = datetime.strptime(fecha, '%Y-%m-%d').date()
        prestamos = prestamos.filter(FechaPrestamo=fecha_seleccionada)

    context = {
        'prestamos': prestamos,
        'encargados': encargados,
        'libros': libros,
        'estudiantes': estudiantes,
        'penalizaciones': penalizaciones,
    }

    return render(request, 'Consultar_prestamos.html', context)

def registrar_entrega(request):
    if request.method == 'POST':
        Id_Prestamo = request.POST["prestamo"]
        Fecha_entrega = request.POST["fecha_entrega"]
        Estado = request.POST["estado"]

        prestamo = Prestamo.objects.get(IdPrestamo=Id_Prestamo)

        # Crear el registro de entrega o devolución
        devolucion = Devolucion.objects.create(IdPrestamo=prestamo, Fecha_entrega=Fecha_entrega, Estado=Estado)
        return redirect('/Entregas')  # Redirigir a la página de gestión de entregas

    # Si la solicitud no es de tipo POST, renderizar la página de inserción de entrega o devolución
    prestamos = Prestamo.objects.all()

    context = {
        'prestamos': prestamos,
    }
    return render(request, 'Gestion_entregas.html', context)
from datetime import date
from django.http import JsonResponse
from .models import Devolucion, Penalizacion

def actualizar_penalizacion(request):
    # Obtener la fecha actual del sistema
    fecha_actual = date.today()
    
    # Obtener las devoluciones con estado "No entregado", sin fecha de entrega y fecha de devolución vencida
    devoluciones = Devolucion.objects.filter(Estado='No entregado', Fecha_entrega=None, IdPrestamo__FechaDevolucion__lt=fecha_actual)
    
    for devolucion in devoluciones:
        # Obtener la penalización del estudiante relacionado
        penalizacion = Penalizacion.objects.get(IdEstudiante=devolucion.IdPrestamo.IdEstudiante)
        # Actualizar el estado de la penalización a "Moroso"
        penalizacion.Estado = 'Moroso'
        penalizacion.save()
    
    return JsonResponse({'success': True})


def buscar_libros(request):
    query = request.GET.get('query', '')
    libros = Libro.objects.filter(titulo__icontains=query).values('titulo')
    return JsonResponse({'libros': list(libros)})

def buscar_estudiantes(request):
    query = request.GET.get('query', '')
    estudiantes = Estudiante.objects.filter(nombre__icontains=query).values('nombre')
    return JsonResponse({'estudiantes': list(estudiantes)})
    
def editar_penalizacion(request, id_penalizacion):
    penalizacion = get_object_or_404(Penalizacion, IdPenalizacion=id_penalizacion)

    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_final = request.POST['fecha_final']
        estado = request.POST['estado']

        # Actualizar los campos de la penalización
        penalizacion.Falseecha_inicio = fecha_inicio
        penalizacion.Fecha_final = fecha_final
        penalizacion.Estado = estado
        penalizacion.save()



        return redirect('/penalizaciones', id_penalizacion=penalizacion.IdPenalizacion)
    penalizaciones = Penalizacion.objects.all()
    context = {
        'penalizaciones': penalizaciones,
    }

    return render(request, 'editar_penalizacion.html', {'penalizacion': penalizacion})


def eliminarprestamo(request, IdPrestamo):
    prestamo= Prestamo.objects.get(IdPrestamo=IdPrestamo)
    prestamo.delete()
    return redirect('/home')

def eliminarentrega(request, IdDevolucion):
    entrega= Devolucion.objects.get(IdDevolucion=IdDevolucion)
    entrega.delete()
    return redirect('/Entregas')

def eliminarpenalizacion(request, IdPenalizacion):
    penalizar= Penalizacion.objects.get(IdPenalizacion=IdPenalizacion)
    penalizar.delete()
    return redirect('/penalizaciones')

def insertar_prestamo(request):
    prestamo = Prestamo.objects.all()
    encargados = Encargado.objects.all()
    libros = Libro.objects.all()
    penalizaciones = Penalizacion.objects.all()

    url = 'http://127.0.0.1:8080/estudiantes/' 
    response = requests.get(url)
    estudiantes = response.json()

    context = {'prestamo': prestamo,'encargados': encargados,'libros': libros,'estudiantes': estudiantes,'penalizaciones': penalizaciones,}

    return render(request, 'ingresar_prestamos.html', context)

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

from django.shortcuts import get_object_or_404

def editar_entrega(request, IdDevolucion):
    if request.method == 'POST':
        entrega = Devolucion.objects.get(IdDevolucion=IdDevolucion)
        prestamos = Prestamo.objects.all()

        entrega.Fecha_entrega = request.POST['fecha_entrega']
        entrega.Estado = request.POST['estado']

        id_prestamo = int(request.POST['prestamo'])
        prestamo = get_object_or_404(Prestamo, IdPrestamo=id_prestamo)
        entrega.IdPrestamo = prestamo

        entrega.save()

        # Verificar si el estado es "Entregado" y actualizar la cantidad del libro
        if entrega.Estado == "Entregado":
            libro = prestamo.IdLibro
            libro.Cantidad += 1
            libro.save()

            # Actualizar el estado de la tabla penalizacion a "Apto"
            id_estudiante = prestamo.IdEstudiante_id
            penalizacion = Penalizacion.objects.get(IdEstudiante_id=id_estudiante)
            penalizacion.Estado = "Apto"
            penalizacion.save()

        return redirect('/Entregas')

    entrega = Devolucion.objects.get(IdDevolucion=IdDevolucion)
    prestamos = Prestamo.objects.all()
    context = {
        'devolucion': entrega,
        'prestamos': prestamos
    }
    return render(request, 'Editar_entrega.html', context)


def listar_libros(request):
    libros = Libro.objects.all()
    context = {
        'libros': libros
    }
    return render(request, 'listar_libros.html', context)

