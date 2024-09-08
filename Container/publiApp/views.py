import time
from django.conf import settings
from django.forms import DateField
from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponse
from django.views.generic import TemplateView

from datetime import timedelta
from django.utils import timezone
from requests import request

from .forms                         import ClientesForm, ContratoForm#, PagosForm
from django.shortcuts               import HttpResponse
from django.urls                    import reverse_lazy
from django.views.generic.list      import ListView
from django.views.generic.detail    import DetailView
from django.views.generic.edit      import CreateView, UpdateView, DeleteView
from django.views                   import View
from .models                        import Cliente, Contrato,Pagos,CustomSession

from django.db.models import Max, F, ExpressionWrapper ,Value

#from . import models
from django.db.models import IntegerField
from django.db.models.functions import Coalesce, Extract, TruncDay, Trunc

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

from django.utils.timesince import timesince
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session as DjangoSession

# Create your views here.



class ClientesBaseView(View):
    """ESTA CLASE NO SE PONE EN LAS URLS"""
    model         = Cliente
    fields        = "__all__"
    success_url = reverse_lazy("publicidad:clientes_all")

class ClientesListView(ClientesBaseView,ListView):
    template_name = "clientes_view.html"
    context_object_name= "clientes"

"""    def get_queryset(self):
        return self.model.objects.filter(activo=True) """


class ClientesUpdateView(ClientesBaseView,UpdateView):
    template_name = "clientes_update.html"
    extra_context={"Titulo" : "Actualiza Clientes",
                   "tipo": "Actualiza"}


def Cliente_Update(request, pk):
    cliente = Cliente.objects.get(id=pk)
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        activo = request.POST['activo']
        video = request.FILES.get('video')
        cliente.nombre = nombre
        cliente.email = email
        cliente.activo = activo
        cliente.video = video
        cliente.save()
        return redirect('publicidad:clientes_all')
    if request.method == 'GET':
        return render(request, 'clientes_update.html',{'cliente':cliente,'tipo':'Actualiza'})

class ClientesCreate(CreateView):
    model = Cliente
    form_class = ClientesForm
    template_name = "clientes_form.html"

    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nuevo_cliente = Cliente(
                username = form.cleaned_data['username'],
                nombre = form.cleaned_data['nombre'],
                email = form.cleaned_data['email'],
                video = form.cleaned_data['video'],
            )
            nuevo_cliente.set_password(form.cleaned_data['password1'])
            nuevo_cliente.save()
            return redirect('publicidad:clientes_all')
        else:
            return render(request, self.template_name, {'form': form})


        

#///////////////// C O N T R A T O //////////////////

def Contrato_Create(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            print("formulario no valido")
            form.save()
        else:
            print("formulario no valido")
        return redirect('publicidad:contratos_list')
    else:
        form = ContratoForm

    return render(request, 'contrato_form.html',{'form':form})

class ContratoBaseView(View):
    """ESTA CLASE NO SE PONE EN LAS URLS"""
    model         = Contrato
    fields        = "__all__"
    success_url = reverse_lazy("publicidad:contratos_list")

class ContratoListView(ContratoBaseView,ListView):
    template_name = "contrato_view.html"
    context_object_name= "contratos"



from datetime import datetime

def contrato_update(request, pk):
    contrato = Contrato.objects.get(id=pk)
    if request.method == 'POST':
        fecha_original = request.POST['fechaVencimientoActual']
        cuota = request.POST['cuota']
        dispositivos = request.POST['dispositivos']
        debe = request.POST['debe']
        contrato.fechaVencimientoActual = fecha_original
        contrato.cuota = cuota
        contrato.dispositivos = dispositivos
        contrato.debe = debe
        contrato.save()
        return redirect('publicidad:contratos_list')
    if request.method == 'GET':
        return render(request, 'contrato_update.html',{'contrato':contrato,'tipo':'Actualiza'})

# /////// pagos //////////

class PagosBaseView(View):
    """ESTA CLASE NO SE PONE EN LAS URLS"""
    model         = Pagos
    fields        = "__all__"
    success_url = reverse_lazy("publicidad:pagos_all")

class PagosListView(PagosBaseView,ListView):
    template_name = "pagos_view.html"
    context_object_name= "pagos"


    
# views.py
from django.shortcuts import render, redirect

from.models import Pagos, Cliente

def busca_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombrebuscado')
        clientes = Cliente.objects.all()
        cliente = Cliente.objects.filter(nombre=nombre)
        if cliente.exists():  # Check if the query returns at least one result
            cliente_id = cliente.first().id  # Get the ID of the first matching cliente
            contrato = Contrato.objects.filter(nombre=cliente_id)
            if contrato:
                vencimiento = contrato.first().fechaVencimientoActual
                saldo = contrato.first().cuota
            return render(request, 'pagos_create.html', {'cliente': nombre, 'vencimiento': vencimiento, 'saldo': saldo,'id':cliente_id})
    return render(request, 'pagos_create.html', {'clientes': clientes})  # o devuelve un mensaje de error

def pagos_create(request):
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        nombreid = request.POST.get('id')
        nombre = request.POST.get('nombre')
        fechaVencimiento = request.POST.get('fechaVencimiento')
        saldo = request.POST.get('saldo')
        fechaPago = request.POST.get('fechaPago')
        pago = request.POST.get('pago')
        if all([nombre, fechaVencimiento, saldo, fechaPago, pago]):
            # Procesa la entrada del usuario
            cliente = Cliente.objects.get(id=int(nombreid))  # Obtener el objeto Cliente
            contrato = Contrato.objects.get(nombre=cliente)  # Asignar el objeto Cliente a contrato
            contrato.fechaVencimientoActual = contrato.fechaVencimientoActual + timedelta(days=30)
            contrato.debe = False
            contrato.save()
            pago = Pagos(nombre=cliente, fechaVencimiento=fechaVencimiento, saldo=saldo, fechaPago=fechaPago, pago=int(pago))
            pago.save()
            return redirect('publicidad:pagos_list')
        else:
            return render(request, 'pagos_create.html', {'error': 'Por favor, complete todos los campos'})
    return render(request, 'pagos_create.html', {'clientes': clientes})

def pagos_update(request, pk):
    pagos = Pagos.objects.get(id=pk)
    if request.method == 'POST':
        fecha_original = request.POST['fechaPago']
        # CONVIERTE EL FORMATO DE FECHA DE dd/mm/aaaa a aaaa-mm-dd para que tome la actualizacion
        fecha = datetime.strptime(fecha_original, "%d/%m/%Y").strftime("%Y-%m-%d")
        pago = request.POST['pago']
        pagos.fechaPago = fecha
        pagos.pago = pago
        pagos.save()
        return redirect('publicidad:pagos_list')
    if request.method == 'GET':
        return render(request, 'pagos_update.html',{'pagos':pagos,'tipo':'Actualiza'})
    
def pagos_delete(request,pk):
    pagos = Pagos.objects.get(id=pk)
    pagos.delete()
    return redirect('publicidad:pagos_list')

import moviepy.editor as mp
from moviepy.editor import *
import os


def video_list(request):
    clientes_activos = Cliente.objects.filter(activo=True,usuario_administrador=False)
    videos = clientes_activos.values_list('video', flat=True)
    clips = []
    #Itera sobre los videos y crea un clip para cada uno
    media_dir = 'static/media/'

    for video in videos:
        if video:  # Verificar si el archivo de video no está vacío
            video_path = os.path.join(media_dir, video)
            if os.path.isfile(video_path):  # Verificar si el archivo existe
                clip = mp.VideoFileClip(video_path)
                clips.append(clip)

    if clips:  # Verificar si hay clips para concatenar
        final_video = mp.concatenate_videoclips(clips)
        final_video.write_videofile(os.path.join(settings.MEDIA_ROOT, '', 'video.mp4'))
    
    #return redirect('Landing_page')
    return HttpResponse("La tarea de procesamiento de videos se está ejecutando en segundo plano.")

class index(View):
    model = Cliente
    fields        = "__all__"
    template_name = "index.html"
    context_object_name= "clientes"


@login_required
def get_active_sessions(request):
    # Filtra sesiones activas basadas en la expiración en CustomSession
    active_sessions = CustomSession.objects.filter(expires_at__gte=timezone.now())

    # Obtiene usuarios basados en las sesiones activas
    user_ids = [s.user_id for s in active_sessions if s.user_id]
    users = Cliente.objects.filter(id__in=user_ids)

    # Obtén sesiones activas de django_session
    django_sessions = DjangoSession.objects.filter(expire_date__gte=timezone.now())

    # Prepara los datos para el template
    sessions_data = [
        {
            'session_key': session.session_key,
            'expire_date': session.expire_date
        }
        for session in django_sessions
    ]

    # Función para calcular el tiempo desde la última actividad
    def get_session_time(session):
        return timesince(session.last_activity)

    # Pasa la lista de sesiones activas y la función para el cálculo del tiempo
    context = {
        'users': users,
        'active_sessions': active_sessions,
        'sessions_data': sessions_data,
        'get_session_time': get_session_time,
    }

    return render(request, 'sesiones_activas.html', context)

"""
@login_required
def finalizar_sesion(request, user_id):
    # Obtiene todas las sesiones activas
    sessions = CustomSession.objects.filter(expires_at__gte=timezone.now())

    # Encuentra y elimina la sesión correspondiente al usuario especificado
    for s in sessions:
        if s.user_id == user_id:
            s.delete()
            break

    return redirect('publicidad:sesiones_activas')  # Redirige a la página de sesiones activas


def guardar_datos_sesion(request, clave, valor):
    if request.custom_session:
        session_data = request.custom_session.data
        session_data[clave] = valor
        request.custom_session.data = session_data
        request.custom_session.save()

def leer_datos_sesion(request, clave):
    if request.custom_session:
        return request.custom_session.data.get(clave)
    return None

def eliminar_sesion(request):
    if request.custom_session:
        request.custom_session.delete()
"""