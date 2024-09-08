from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth import logout

from .views import video_list
from .models import CustomSession, Cliente
from django.contrib.auth.signals import user_logged_out
import pytz

User = get_user_model()
"""
@shared_task
def detectar_usuarios_inactivos():
    # Calcula el tiempo límite de inactividad usando zona horaria "aware"
    limite_inactividad = timezone.now() - timedelta(minutes=5)
    print(f'limite de inactividad {limite_inactividad}')
    # Filtra las sesiones de usuarios inactivos basadas en last_activity
    sesiones_inactivas = CustomSession.objects.filter(last_activity__lt=limite_inactividad)
    
    usuarios_inactivos = {}  # Para almacenar la información de usuarios y sus sesiones inactivas
    
    # Itera sobre las sesiones inactivas para realizar una acción
    for sesion in sesiones_inactivas:
        usuario_id = sesion.user_id
        if not usuario_id:
            continue  # En caso de que la sesión no esté asociada a un usuario
        
        if usuario_id not in usuarios_inactivos:
            usuarios_inactivos[usuario_id] = []
        
        usuarios_inactivos[usuario_id].append(sesion)
    
    # Procesa cada usuario inactivo
    for usuario_id, sesiones in usuarios_inactivos.items():
        user = Cliente.objects.filter(id=usuario_id).first()
        if not user:
            continue
        
        # Verifica si todas las sesiones están inactivas
        sesiones_inactivas = [sesion for sesion in sesiones if sesion.last_activity < limite_inactividad]
        if sesiones_inactivas:
            # Realiza el logout manual
            user_logged_out.send(sender=user.__class__, request=None, user=user)
            
            # Elimina solo las sesiones inactivas del usuario
            CustomSession.objects.filter(user=usuario_id, last_activity__lt=limite_inactividad).delete()
            
            mensaje = f'El usuario {usuario_id} ha excedido el límite de actividad y sus sesiones inactivas fueron borradas'
        else:
            mensaje = f'El usuario {usuario_id} está activo'
        
        print(mensaje)  # o realizar alguna otra acción, como enviar un correo electrónico
    
    return "Tiempo de inactividad a testear > 5 min --"
"""


@shared_task
def crea_video():
    video_list()
    