from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cliente', views.serviciosCliente, name='cliente'),
    path('consultaCliente', views.consultaCliente, name='consultaCliente'),
    path('crearCarta', views.CrearCarta, name='crearCarta'),
    path('editarCarta/<int:id>', views.editarCarta, name='editarCarta'),
    path('solicitud', views.solicitud, name='solicitud'),
    path('consultar/<int:id>', views.consultaCliente, name='consultaCliente'), 
    path('ingresar', views.ingresar, name='ingresar'),
    path('trabajador', views.crearDatos, name='trabajador'),
    path('consultaCarta/<int:id>', views.consultaCarta, name='consultaCarta'),
    path('consultaCarta/<int:id>/eliminar', views.eliminar_carta, name='eliminar'),
    path('salir', views.salir, name='salir'),


]
