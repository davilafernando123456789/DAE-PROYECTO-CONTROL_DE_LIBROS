from django.urls import path
from.import views

urlpatterns=[
    path('',views.login_view),
    path('home',views.listarPrestamos, name='listarPrestamos'),
    path('Entregas',views.listarEntrega),
    path('Libros', views.listar_libros, name='listar_libros'),
    path('insertar_prestamo', views.insertar_prestamo, name='insertar_prestamo'),
    path('registrar_prestamo', views.prestamo_form, name='registrar_prestamo'),
    path('eliminarprestamo/<IdPrestamo>',views.eliminarprestamo),
    path('editar_prestamo/<IdPrestamo>', views.editar_prestamo),
    path('registrar_entrega', views.registrar_entrega, name='registrar_entrega'),
    path('eliminarentrega/<IdDevolucion>',views.eliminarentrega),
    path('editar_entrega/<IdDevolucion>', views.editar_entrega),
    path('penalizaciones/', views.listar_editar_penalizacion, name='listar_editar_penalizacion'),
    path('editar_penalizacion/<int:id_penalizacion>/', views.editar_penalizacion, name='editar_penalizacion'),
    path('eliminarpenalizacion/<IdPenalizacion>',views.eliminarpenalizacion),
      # otras rutas de tu aplicación
    path('buscar_libros/', views.buscar_libros, name='buscar_libros'),
    path('buscar_estudiantes/', views.buscar_estudiantes, name='buscar_estudiantes'),
    # listar estudiantes mediante API   
    path('listar_estudiantes/', views.Listar_estudiantes, name='listar_estudiantes'),
]
