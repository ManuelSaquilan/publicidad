from django.shortcuts import redirect, render
from django.views.generic           import TemplateView
from datetime import timedelta, date



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
    
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

