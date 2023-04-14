import datetime

from django.views.generic import (
    TemplateView
)

class HomePage(TemplateView):
    template_name = "home/panel.html"

class FechaMixin(object):
    """ Ejemplo de los Mixin"""
    
    def get_context_data(self, **kwargs):
        """" Manda en un contexto lo que se quiere reutilizar, para utilizarlo solo se debe
        poner el nombre de la clave del contexto """
        
        context = super(FechaMixin, self).get_context_data(**kwargs)
        print(context,"**********")
        context['fecha'] = datetime.datetime.now()
        context['loca'] = "LOCA LOCA LOCA"
        print(context)
        return context
    

class TemplatePruebaMixin(FechaMixin, TemplateView):
    template_name = "home/mixin.html"
