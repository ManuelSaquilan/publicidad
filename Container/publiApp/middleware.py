import datetime
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render

from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import CustomSession
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.deprecation import MiddlewareMixin

"""
class SessionLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_request(self, request):
        print("process_request")
        if request.user.is_authenticated:
            user = request.user
            max_sessions = user.contrato.dispositivos
            active_sessions = self.get_active_sessions(request)
            print("sesiones activas: ",active_sessions)
            if len(active_sessions) >= max_sessions:
                # si el usuario tiene demasiadas sesiones activas, cerramos la sesión actual
                request.session.flush()
                return HttpResponseForbidden("Too many active sessions")
            else:
                # actualizamos la última actividad de la sesión
                request.session['last_activity'] = datetime.datetime.now()

    def get_active_sessions(self, request):
        # devuelve una lista de sesiones activas del usuario
        sessions = []
        print("get_active_sessiones")
        for session in Session.objects.all():
            if session.get_decoded().get('_auth_user_id') == request.user.id:
                last_activity = session.get_decoded().get('last_activity')
                if last_activity and (datetime.datetime.now() - last_activity).total_seconds() < 300:  # 5 minutos de inactividad
                    sessions.append(session)
        return sessions
"""

from django.contrib.auth import logout
from django.contrib import messages
import datetime
from django.http import HttpResponse

class SessionLimitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and not request.user.usuario_administrador:
            # Verificar si el usuario tiene sesiones activas
            active_sessions = CustomSession.objects.filter(user=request.user)
            
            # Si el número de sesiones activas supera el límite permitido por el contrato
            if active_sessions.count() > request.user.contrato.dispositivos:
                # Cerrar la sesión más antigua en lugar de la primera, para mantener la sesión más reciente
                session_to_delete = active_sessions.order_by('last_activity').first()
                
                if session_to_delete:
                    try:
                        session_to_delete.delete()
                    except CustomSession.DoesNotExist:
                        pass
                    
                    # Cerrar la sesión actual solo si es la misma que la eliminada
                    if session_to_delete.session_key == request.COOKIES.get('sessionid'):
                        logout(request)
                        messages.add_message(request, messages.WARNING, 'Ha superado el límite de sesiones permitidas.')
                        return None  # O redirige si es necesario

        return None  # Continua con el procesamiento normal de la solicitud
    
User = get_user_model()

class CustomSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_key = request.COOKIES.get('sessionid')
        request.custom_session = None

        if session_key:
            try:
                session = CustomSession.objects.get(session_key=session_key, expires_at__gt=timezone.now())
                request.custom_session = session
                # Actualiza last_activity solo si la sesión está asociada y válida
                session.last_activity = timezone.now()
                session.save()
            except CustomSession.DoesNotExist:
                pass

        response = self.get_response(request)

        return response
        
# Receptores de señales para manejar la asociación y limpieza de sesiones

@receiver(user_logged_in)
def asociar_sesion_con_usuario(sender, request, user, **kwargs):
    session_key = request.COOKIES.get('sessionid')
    if session_key:
        try:
            session = CustomSession.objects.get(session_key=session_key)
            session.user = user
            session.save()

            expira = timezone.now() + timedelta(seconds=180)
            response = JsonResponse({'status': 'success'})
            response.set_cookie('sessionid', session_key, expires=expira)
            request.session.set_expiry(expira)
        except CustomSession.DoesNotExist:
            pass

@receiver(user_logged_out)
def desasociar_sesion_de_usuario(sender, request, user, **kwargs):
    session_key = request.COOKIES.get('sessionid')
    if session_key:
        try:
            session = CustomSession.objects.get(session_key=session_key)
            session.user = None  # Desasociar usuario en el logout
            session.save()
        except CustomSession.DoesNotExist:
            pass
