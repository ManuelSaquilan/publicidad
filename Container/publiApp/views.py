from django.conf import settings
from django.forms import DateField
from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponse
from django.views.generic import TemplateView

from datetime import timedelta
from django.utils import timezone

from .forms                         import ClientesForm, ContratoForm#, PagosForm
from django.shortcuts               import HttpResponse
from django.urls                    import reverse_lazy
from django.views.generic.list      import ListView
from django.views.generic.detail    import DetailView
from django.views.generic.edit      import CreateView, UpdateView, DeleteView
from django.views                   import View
from .models                        import SessionInfo, Cliente, Contrato,Pagos

from django.db.models import Max, F, ExpressionWrapper ,Value

#from . import models
from django.db.models import IntegerField
from django.db.models.functions import Coalesce, Extract, TruncDay, Trunc

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

from django.utils.timesince import timesince
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
    clientes_activos = Cliente.objects.filter(activo=True)
    print(clientes_activos)
    videos = clientes_activos.values_list('video', flat=True)
    clips = []
    print(videos)
    #Itera sobre los videos y crea un clip para cada uno
    media_dir = 'static/media/'

    for video in videos:
        video_path = os.path.join(media_dir, video)
        clip = mp.VideoFileClip(video_path)
        print(clip)
#        clip = mp.VideoFileClip(video[0])
        clips.append(clip)
#        # Concatena los clips de video
        final_video = mp.concatenate_videoclips(clips)
#
 #       # Guarda el video final
        final_video.write_videofile(os.path.join(settings.MEDIA_ROOT, '', 'video.mp4'))
    return redirect('Landing_page')

class index(View):
    model = Cliente
    fields        = "__all__"
    template_name = "index.html"
    context_object_name= "clientes"





from django.views.decorators.http import require_GET
"""
@require_GET
def ping_view(request):
    
    request.user.cliente.last_ping = timezone.now()
    request.user.cliente.save()
    request.user.last_ping = timezone.now()
    request.user.save()
    return HttpResponse('OK')
"""

def get_active_sessions(request):
    active_sessions = Session.objects.filter(expire_date__gte=datetime.now())
    users = Cliente.objects.filter(id__in=[s.get_decoded().get('_auth_user_id') for s in active_sessions])

    def get_session_time(session):
        delta = datetime.now() - session.expire_date
        return timesince(delta)

    return render(request, 'sesiones_activas.html', {'users': users, 'active_sessions': active_sessions, 'get_session_time': get_session_time})

def finalizar_sesion(request, user_id):
    sessions = Session.objects.filter(expire_date__gte=datetime.now())
    for s in sessions:
        if s.get_decoded().get('_auth_user_id') == user_id:
            s.delete()
            break
    return redirect('publicidad:sesiones_activas')  # Redirige a la página de sesiones activas