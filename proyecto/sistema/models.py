from django.db import models
from django.contrib.auth.models import User


#crear tablas en bd
# Create your models here.
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    ciudad = models.CharField(max_length=100, verbose_name='Ciudad')
    motivo = models.TextField(verbose_name='Motivo de la carta')
    correo = models.EmailField(verbose_name='Correo')

    def __str__(self):
        fila = "Nombre: " + self.nombre + " - " + "Ciudad: " + self.ciudad + " - " + "Motivo: " + self.motivo + " - " + "Correo: " + self.correo
        return fila
    


class EstadoTrabajador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre')

    def __str__(self):
        fila = "Nombre: " + self.nombre
        return fila 
    
    
class Trabajador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    edad = models.CharField(max_length=100, verbose_name='edad')
    estadoTra = models.ForeignKey(EstadoTrabajador, on_delete=models.CASCADE, verbose_name="Estado")

    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    def __str__(self):
        fila = "Nombre: " + self.nombre + " - " + "Edad: " + self.edad
        return fila
    

class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre')

    def __str__(self):
        fila = "Nombre: " + self.nombre
        return fila

class Carta(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador")
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name="Estado")
    contenido = models.TextField(verbose_name="Contenido")

    def __str__(self):
        return f"Carta de {self.cliente.nombre} atendida por {self.trabajador.nombre} - Estado: {self.estado.nombre}"


#prueba git