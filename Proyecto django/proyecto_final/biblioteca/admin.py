from django.contrib import admin
from .models import Autor, Categoria, Credenciales, Editorial, Encargado, Estudiante, Libro, Prestamo, Penalizacion, Devolucion

class AutorAdmin(admin.ModelAdmin):
    list_display = ('IdAutor', 'Nombre', 'Genero', 'Apellido', 'Fecha_nacimiento', 'Nacionalidad')

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('Idcategoria', 'Nombre')

class CredencialesAdmin(admin.ModelAdmin):
    list_display = ('IdCredenciales', 'Usuario', 'Contraseña')

class EditorialAdmin(admin.ModelAdmin):
    list_display = ('idEditorial', 'Nombre', 'Telefono', 'Correo', 'Pais', 'Ciudad', 'Direccion')

class EncargadoAdmin(admin.ModelAdmin):
    list_display = ('IdEncargado', 'Nombre', 'Apellido', 'Direccion', 'Telefono', 'Correo', 'IdCredenciales')

class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('IdEstudiante', 'Nombre', 'Apellido', 'DNI', 'Direccion', 'Telefono', 'Correo')

class LibroAdmin(admin.ModelAdmin):
    list_display = ('IdLibro', 'Titulo', 'ISBN', 'Autor', 'Editorial', 'Categoria', 'Año_publicacion', 'Disponibilidad')

class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('IdPrestamo', 'IdEncargado', 'IdLibro', 'IdEstudiante', 'FechaPrestamo', 'FechaDevolucion')

class DevolucionAdmin(admin.ModelAdmin):
    list_display = ('IdDevolucion', 'IdPrestamo', 'Fecha_entrega', 'Estado')

class PenalizacionAdmin(admin.ModelAdmin):
    list_display = ('IdPenalizacion', 'IdEstudiante', 'Falseecha_inicio', 'Fecha_final', 'Estado')

admin.site.register(Autor, AutorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Credenciales, CredencialesAdmin)
admin.site.register(Editorial, EditorialAdmin)
admin.site.register(Encargado, EncargadoAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Prestamo, PrestamoAdmin)
admin.site.register(Devolucion, DevolucionAdmin)
admin.site.register(Penalizacion, PenalizacionAdmin)
