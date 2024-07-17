from datetime import timedelta

from django.utils import timezone

from Container.publiApp.models import Cliente
from celery import shared_task

"""

@shared_task
def restar_conexiones():
    timeout = timezone.now() - timedelta(minutes=5)
    clientes = Cliente.objects.filter(last_ping__lt=timeout)
    for cliente in clientes:
        print (cliente.nombre)
        cliente.connection_count -= 1
        cliente.save()
        from django.contrib.auth import logout
        logout(cliente.usuario)

        """