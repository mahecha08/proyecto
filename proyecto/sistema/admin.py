from django.contrib import admin
from .models import Cliente
from .models import Carta
from .models import Estado
from .models import Trabajador # se implementa
from .models import EstadoTrabajador # se implementa

admin.site.register(Cliente)
admin.site.register(Trabajador)
admin.site.register(Estado)
admin.site.register(Carta)
admin.site.register(EstadoTrabajador)
# Register your models here.
