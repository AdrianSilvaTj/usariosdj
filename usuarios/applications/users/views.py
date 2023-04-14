from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import (
    View, TemplateView
)
from django.views.generic.edit import FormView

from .forms import UserRegisterForm, LoginForm
from .models import User

class UserRegisterView(FormView):
    """ Vista que toma los datos y crea el usuario en la base de datos """
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'
    
    def form_valid(self, form):
        
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            first_name = form.cleaned_data['first_name'],
            last_name = form.cleaned_data['last_name'],
            gender = form.cleaned_data['gender'],
        )
        
        return super(UserRegisterView, self).form_valid(form)
    
class LoginView(FormView):
    """ Vista donde se autentican los datos del login y se realiza el mismo """
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('users:panel')
    
    def form_valid(self, form):
        """ Una vez validados los datos, hace el login del usuario """
        login(self.request, form.cleaned_data['user'])
        return super(LoginView, self).form_valid(form)
    
class HomePageView(LoginRequiredMixin, TemplateView):
    """ Vista para Mostrar el panel de usuario, una vez logeado """
    template_name = "users/panel.html"
    
    # se utiliza para verificar que haya un usuario logeado, en caso contrario
    # lo envía a esa url
    login_url = reverse_lazy('users:login')

class LogoutView(View):
    """ Hace el logout del usuario, esta vista no necesita un template """
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('users:login'))