from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic           import TemplateView
from datetime import datetime, timedelta, date, timezone

from requests import request

from django.http import JsonResponse
from django.utils import timezone
from publiApp.models import CustomSession
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session as DjangoSession
import json



class LandingPage(TemplateView):
    template_name = "bloques/index.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo_pagina"] = "Bienvenida"
        user = self.request.user
        if not(user.is_staff):
            fechalimite = user.contrato.fechaVencimientoActual + timedelta(days=10)
            fechaActual = date.today()
            
            if fechaActual > fechalimite:
                user.contrato.debe = True
                user.contrato.save()
                vencido = True
                mensaje = 'Su abono esta vencido'
            else:
                vencido = False
                mensaje = 'Su abono esta vigente'
            context['vencido'] = vencido
            context['mensaje'] = mensaje
            
            # Contar las sesiones activas para el usuario
            session_count = CustomSession.objects.filter(user=user, expires_at__gt=timezone.now()).count()
            context['connection_count'] = session_count
            
        return context

class Publicidad(TemplateView):
    template_name = "bloques/publicidad.html"
    extra_context = {
        "titulo_pagina" : "Publicidad"
    }

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect



class CustomLoginView(LoginView):

    def form_valid(self, form):
        print("Ejecuto custom login view 2")

        # Autenticación del usuario
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            print("Llego al punto de autenticación")
            login(self.request, user)  # Esto maneja la sesión automáticamente

            # Crear o actualizar la sesión personalizada
            session_key = self.request.session.session_key  # O obtenerla de self.request.COOKIES.get('sessionid')
            if session_key:
                # Verificar si ya existe una CustomSession para este usuario y clave de sesión
                try:
                    session = CustomSession.objects.get(session_key=session_key)
                    session.user = user
                    session.last_activity = timezone.now()
                    session.save()
                except CustomSession.DoesNotExist:
                    # Crear un nuevo registro de CustomSession si no existe
                    CustomSession.objects.create(
                        session_key=session_key,
                        user=user,
                        expires_at=timezone.now() + timedelta(minutes=180),  # Define el tiempo de expiración
                        last_activity=timezone.now()
                    )
            else:
                # Crear una nueva CustomSession si no hay clave de sesión
                new_session = CustomSession(
                    user=user,
                    expires_at=timezone.now() + timedelta(minutes=180),  # Define el tiempo de expiración
                    last_activity=timezone.now()
                )
                new_session.save()
                # Establecer la cookie de sesión personalizada
                self.request.session['sessionid'] = new_session.session_key

            return redirect('Landing_page')  # Redirigir al usuario a la página de inicio
        
        return super().form_invalid(form)


@csrf_exempt  # Decorador para eximir la vista del requerimiento de CSRF
def heartbeat(request):
    if request.method == 'POST':
        session_key = request.COOKIES.get('sessionid')
        #session_key = request.COOKIES.get('custom_session_key')
        if session_key:
            try:
                expira = timezone.now() + timedelta(seconds=300)
                
                # Actualiza CustomSession
                session = CustomSession.objects.get(session_key=session_key)
                session.last_activity = timezone.now()
                session.expires_at = expira
                session.save()
                
                # Actualiza la cookie de sesión
                response = JsonResponse({'status': 'success'})
                expires_at = expira
                response.set_cookie('sessionid', session_key, expires=expires_at)
                request.session.set_expiry(expires_at)
                nueva = request.session.get_expiry_age()
                print(f'La sesion {session_key} del usuario {session.user_id} expira ahora expira en: {nueva} segundos')
                return response
            except CustomSession.DoesNotExist:
                return JsonResponse({'status': 'session not found'}, status=404)
        return JsonResponse({'status': 'no session key'}, status=400)
    return JsonResponse({'status': 'invalid request'}, status=405)  # Solo permite POST
