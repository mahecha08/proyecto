from .models import Cliente, Trabajador, Carta
from django.forms import ModelForm


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class TrabajadorForm(ModelForm):
    class Meta:
        model = Trabajador
        fields = ['nombre', 'edad', 'estadoTra']

class CartaForm(ModelForm):
    class Meta:
        model = Carta
        fields = '__all__'