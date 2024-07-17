from django.views.generic           import TemplateView

from datetime import timedelta, date

class LandingPage(TemplateView):
    template_name = "bloques/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo_pagina"] = "Bienvenida"
        user = self.request.user
        if not(user.is_staff):
            fechalimite = user.contrato.fechaVencimientoActual + timedelta(days=10)
            print('vencimiento',fechalimite)
            fechaActual = date.today()
            print('fechaActual',fechaActual)
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
