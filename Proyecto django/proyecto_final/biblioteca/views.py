from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from .models import Prestamo,Libro,Estudiante,Encargado, Penalizacion, Devolucion
from django.db.models import Q
from django.http import JsonResponse

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
            penalizaciones = Penalizacion.objects.all()
            return render(request, 'Gestion_prestamo.html', {"prestamos":prestamos_listado,"encargados": encargados_listado,"libros":libros_listado,"estudiantes":estudiantes_listado, "penalizaciones": penalizaciones,})  # Reemplaza 'nombre_de_la_pagina' con el nombre de la página a la que deseas redirigir
        else:
            # El usuario no ha proporcionado credenciales válidas
            pass
    
    return render(request, 'login.html')

                  
def home(request):
    prestamos = Prestamo.objects.all()
    encargados = Encargado.objects.all()
    libros = Libro.objects.all()
    estudiantes = Estudiante.objects.all()
    penalizaciones = Penalizacion.objects.all()

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
        'penalizaciones': penalizaciones,
    }
    return render(request, 'listar_editar_penalizacion.html', context)


from datetime import datetime

from datetime import datetime
def insertar_estudiante_en_penalizacion(Id_Prestamo):
    prestamo = Prestamo.objects.get(IdPrestamo=Id_Prestamo)
    devolucion = Devolucion.objects.get(IdPrestamo=prestamo)
    
    # Obtener el objeto Estudiante a través de la relación con Prestamo
    estudiante = prestamo.IdEstudiante
    
    # Verificar si ya existe una penalización para el estudiante
    if Penalizacion.objects.filter(IdEstudiante=estudiante).exists():
        return  # Si ya existe, no hacer nada
    
    # Comparar las fechas de entrega y de devolución
    if devolucion.Fecha_entrega > prestamo.FechaDevolucion:
        # Calcular la fecha final de penalización
        fecha_final_penalizacion = devolucion.Fecha_entrega + timedelta(days=30)

        # Crear un nuevo objeto Penalizacion
        penalizacion = Penalizacion()
        penalizacion.IdEstudiante = estudiante
        penalizacion.Falseecha_inicio = prestamo.FechaDevolucion
        penalizacion.Fecha_final = fecha_final_penalizacion
        penalizacion.Estado = "moroso"
        penalizacion.Falseecha_inicio = datetime.now()  # Asignar un valor a Falseecha_inicio

        # Guardar el objeto Penalizacion en la base de datos
        penalizacion.save()

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
        estudiante = Estudiante.objects.get(IdEstudiante=Id_Estudiante)

        # Crear el registro de préstamo
        prestamo = Prestamo.objects.create(IdEncargado=encargado, IdLibro=libro, IdEstudiante=estudiante,
                                           FechaPrestamo=FechaPrestamo, FechaDevolucion=FechaDevolucion)

        # Obtener la fecha actual

        # Calcular la fecha de entrega
        fecha_entrega = FechaDevolucion # Asumiendo una devolución después de 7 días

        # Crear el registro de devolución
        devolucion = Devolucion.objects.create(IdPrestamo=prestamo, Fecha_entrega=fecha_entrega, Estado="No entregado")

        return redirect('/home')

    prestamos = Prestamo.objects.all()

    # Filtrar los préstamos por nombre de estudiante o título de libro si se proporciona el parámetro de búsqueda
    if query:
        prestamos = prestamos.filter(Q(IdEstudiante__Nombre__icontains=query) | Q(IdLibro__Titulo__icontains=query))
    else:
        prestamos = prestamos.all()

    encargados = Encargado.objects.all()
    libros = Libro.objects.all()
    estudiantes = Estudiante.objects.all()
    penalizaciones = Penalizacion.objects.all()
    devoluciones = Devolucion.objects.all()

    context = {
        'prestamos': prestamos,
        'encargados': encargados,
        'libros': libros,
        'estudiantes': estudiantes,
        'penalizaciones': penalizaciones,
        'devoluciones': devoluciones,
    }

    return render(request, 'Gestion_prestamo.html', context)

def listarPrestamos(request):
    prestamos = Prestamo.objects.all()
    encargados = Encargado.objects.all()
    libros = Libro.objects.all()
    estudiantes = Estudiante.objects.all()
    penalizaciones = Penalizacion.objects.all()

    context = {
        'prestamos': prestamos,
        'encargados': encargados,
        'libros': libros,
        'estudiantes': estudiantes,
        'penalizaciones': penalizaciones,
    }

    return render(request, 'Gestion_prestamo.html', context)

       #try:
            # Obtener el objeto Penalizacion asociado al estudiante
          #  penalizacion = Penalizacion.objects.get(IdEstudiante=Id_Estudiante)

            # Verificar si hay una fecha de inicio y una fecha de fin en la penalización
           # if penalizacion.Falseecha_inicio  and penalizacion.Fecha_final:
           #     penalizacion.calcular_estado()
           # else:
                # Si no hay fecha de inicio ni de fin, el estado es "apto"
            #    penalizacion.Estado = "apto"

            # Guardar los cambios en la base de datos
           # penalizacion.save()

       # except Penalizacion.DoesNotExist:
            # El estudiante no se encuentra en la tabla Penalizacion, no se realiza ninguna acción adicional
         #   pass


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
    estudiantes = Estudiante.objects.all()
    penalizaciones = Penalizacion.objects.all()

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
        return redirect('/editar_prestamo')
    # Si la solicitud es GET, renderizar el formulario de edición con los datos actuales del préstamo
    encargados = Encargado.objects.all()
    libros = Libro.objects.all()
    estudiantes = Estudiante.objects.all()

    context = {'prestamo': prestamo,'encargados': encargados,'libros': libros,'estudiantes': estudiantes,}

    return render(request, 'Editar_Prestamo.html', context)

def editar_entrega(request, IdDevolucion):
    if request.method == 'POST':
        entrega = Devolucion.objects.get(IdDevolucion=IdDevolucion)
        prestamos = Prestamo.objects.all()

        entrega.Fecha_entrega = request.POST['fecha_entrega']
        entrega.Estado = request.POST['estado']

        id_prestamo = int(request.POST['prestamo'])
        prestamo = Prestamo.objects.get(IdPrestamo=id_prestamo)
        entrega.IdPrestamo = prestamo

        entrega.save()
        insertar_estudiante_en_penalizacion(Id_Prestamo=entrega.IdPrestamo.IdPrestamo)

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