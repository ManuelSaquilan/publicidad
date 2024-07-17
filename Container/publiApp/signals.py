from django.utils import timezone
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.apps import apps



@receiver(user_logged_in)
def incrementar_conexion_usuario(sender, user, request, **kwargs):
    Cliente = apps.get_model('publiApp', 'Cliente')
    user.connection_count += 1
    user.last_activity = timezone.now()
    user.save()


@receiver(user_logged_out)
def decrementar_conexion_usuario(sender, user, request, **kwargs):
    Cliente = apps.get_model('publiApp', 'Cliente')
    user.connection_count -= 1
    user.save()
    
"""
from django.shortcuts import get_object_or_404
from publiApp.models import Cliente

@receiver(user_logged_out)
def decrementar_conexion_usuario(sender, user, request, **kwargs):
    cliente = get_object_or_404(Cliente, usuario_administrador=user)
    cliente.connection_count -= 1
    cliente.save()

"""