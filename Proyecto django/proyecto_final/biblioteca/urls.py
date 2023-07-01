from django.urls import path
from.import views

urlpatterns=[
    path('',views.login_view),
    path('home',views.home),
    path('/home',views.home),
    path('registrar_prestamo', views.prestamo_form, name='registrar_prestamo'),
    path('eliminarprestamo/<IdPrestamo>',views.eliminarprestamo),
    path('editar_prestamo/<IdPrestamo>', views.editar_prestamo),
]