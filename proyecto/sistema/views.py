from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Cliente, Trabajador, Estado, Carta, EstadoTrabajador # se importa
from .forms import ClienteForm, TrabajadorForm, CartaForm # se importa
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

def inicio(request):
    return render(request, 'paginas/index.html')

@login_required
def serviciosCliente(request):
    query_nombre = request.GET.get('nombre', '')
    query_ciudad = request.GET.get('ciudad', '')

    cliente = Cliente.objects.all()

    if query_nombre:
        cliente = cliente.filter(nombre__icontains=query_nombre)
    if query_ciudad:
        cliente = cliente.filter(ciudad__icontains=query_ciudad)

    return render(request, 'cliente/index.html', {
        'cliente': cliente,
        'query_nombre': query_nombre,
        'query_ciudad': query_ciudad,
    })

@login_required
def consultaCliente(request, id):
    consulta = Cliente.objects.get(id=id)
    return render(request, 'cliente/cosultaCliente.html', {'consulta': consulta})

@login_required
def CrearCarta(request):
    trabajador = get_object_or_404(Trabajador, user=request.user)

    if trabajador.estadoTra.nombre.lower() == "inactivo":
        messages.error(request, "No puedes crear más cartas. Estás inactivo.")
        return redirect('cliente')

    cartas_pendientes = Carta.objects.filter(
        trabajador=trabajador,
        estado__nombre__in=["borrador", "revisado"]
    ).count()

    if cartas_pendientes >= 5:
        estado_inactivo = EstadoTrabajador.objects.get(nombre__iexact="inactivo")
        trabajador.estadoTra = estado_inactivo
        trabajador.save()
        messages.error(request, "Has alcanzado el límite de 5 cartas en borrador/revisado. Tu estado ahora es INACTIVO.")
        return redirect('cliente')

    if request.method == 'POST':
        form = CartaForm(request.POST)
        if form.is_valid():
            carta = form.save(commit=False)
            carta.trabajador = trabajador
            carta.save()

            cartas_pendientes = Carta.objects.filter(
                trabajador=trabajador,
                estado__nombre__in=["borrador", "revisado"]
            ).count()

            if cartas_pendientes >= 5:
                estado_inactivo = EstadoTrabajador.objects.get(nombre__iexact="inactivo")
                trabajador.estadoTra = estado_inactivo
                trabajador.save()
                messages.warning(request, "Has alcanzado el límite. Ya no podrás crear más cartas hasta despejar algunas.")

            return redirect('consultaCarta', id=carta.cliente.id)
    else:
        form = CartaForm()

    return render(request, 'cliente/crear.html', {'form': form})


@login_required
def editarCarta(request, id):
    editar = get_object_or_404(Carta, pk=id)
    trabajador = get_object_or_404(Trabajador, user=request.user)

    if request.method == 'GET':
        form = CartaForm(instance=editar)
        return render(request, 'cliente/editar.html', {'editar': editar, 'form': form})
    else:
        form = CartaForm(request.POST, instance=editar)
        if form.is_valid():
            carta = form.save()

            if carta.estado.nombre.lower() == "enviado":
                asunto = "Tu carta esta aqui"
                html_mensaje = render_to_string("cliente/carta_enviada.html", {
                    "cliente": carta.cliente,
                    "carta": carta,
                })
                mensaje_plano = (
                    f"Hola {carta.cliente.nombre},\n\n"
                    f"Aquí está la información de tu carta:\n\n"
                    f"Trabajador: {carta.trabajador.nombre}\n\n\n"
                    f"Contenido:\n{carta.contenido}\n\n"
                )

                email = EmailMessage(
                    asunto,
                    mensaje_plano,
                    settings.DEFAULT_FROM_EMAIL,
                    [carta.cliente.correo],
                )
                email.content_subtype = "plain"
                email.send(fail_silently=False)

            # Revisión de estado del trabajador
            cartas_pendientes = Carta.objects.filter(
                trabajador=trabajador,
                estado__nombre__in=["borrador", "revisado"]
            ).count()

            if cartas_pendientes < 5:
                estado_activo = EstadoTrabajador.objects.get(nombre__iexact="activo")
                trabajador.estadoTra = estado_activo
                trabajador.save()
                messages.success(request, "Has vuelto a estar ACTIVO. Ya puedes crear nuevas cartas.")

            return redirect('consultaCarta', id=editar.cliente.id)
        else:
            return render(request, 'cliente/editar.html', {'editar': editar, 'form': form})

    
    


def solicitud(request):
    formulario = ClienteForm(request.POST or None)
    if formulario.is_valid():
        cliente = formulario.save()

        asunto = "Confirmación de solicitud"
        mensaje = (
            f"Hola {cliente.nombre},\n\n"
            f"Hemos recibido tu solicitud con el motivo:\n\n"
            f"'{cliente.motivo}'\n\n"
            "Un trabajador la revisará pronto.\n\n"
            "Gracias por confiar en nosotros."
        )
        destinatario = [cliente.correo]

        send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, destinatario, fail_silently=False)

        messages.success(request, "Solicitud registrada y correo enviado exitosamente")
        return redirect('inicio')

    return render(request, 'cliente/solicitud.html', {'formulario': formulario})

@login_required
def crearDatos(request): 
    if request.method == 'GET':
        formulario = TrabajadorForm() 
        return render(request, 'cliente/trabajador.html', {'formulario': formulario})
    else: 
        formulario = TrabajadorForm(request.POST)  
        if formulario.is_valid():
            trabajadorID = formulario.save(commit=False)
            trabajadorID.user = request.user
            trabajadorID.save()
            return redirect('cliente') 
        else:
            return render(request, 'cliente/trabajador.html', {'formulario': formulario})


def ingresar(request):
    if request.method == 'GET':
        return render(request, 'cliente/ingresar.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'cliente/ingresar.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, user)

            if Trabajador.objects.filter(user=user).exists():
                return redirect('cliente')  
            else:
                return redirect('trabajador') 


def salir(request):
    logout(request)
    return redirect('inicio')


def consultaCarta(request, id):
    trabajador = get_object_or_404(Trabajador, user=request.user)

    cartas = Carta.objects.filter(cliente_id=id, trabajador=trabajador)

    cliente = get_object_or_404(Cliente, id=id)

    return render(request, 'cliente/consultaCarta.html', {
        'cartas': cartas,
        'cliente': cliente,
    })

