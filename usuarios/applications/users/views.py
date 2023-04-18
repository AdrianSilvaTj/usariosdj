from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import (
    View, TemplateView
)
from django.views.generic.edit import FormView

from .forms import UserRegisterForm, LoginForm, PasswordUpdateForm, VerificationForm
from .models import User
from .functions import code_generator

class UserRegisterView(FormView):
    """ Vista que toma los datos y crea el usuario en la base de datos """
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'
    
    def form_valid(self, form):
        
        # generamos el código de validación
        code = code_generator()
        
        user_reg = User.objects.create_user(
                        form.cleaned_data['username'],
                        form.cleaned_data['email'],
                        form.cleaned_data['password1'],
                        first_name = form.cleaned_data['first_name'],
                        last_name = form.cleaned_data['last_name'],
                        gender = form.cleaned_data['gender'],
                        is_staff=form.cleaned_data['is_staff'],
                        cod_register = code
                    )
        # enviar código al email del user
        subject = 'Confirmación de email'
        message = 'Código de verificación: '+ code
        email_sender = 'adrian.silva.tj@gmail.com'
        send_mail(subject, message, email_sender, [form.cleaned_data['email']])
        # redirigir a pantalla de validación, pasamos el id por parámetro a la url
        print(user_reg.id)
        return HttpResponseRedirect(
            reverse('users:verification', kwargs={'pk':user_reg.id})            
            )
        
        #return super(UserRegisterView, self).form_valid(form)
    
class VerificationView(FormView):
    """ Vista donde se verifica el codigo enviado para el registro de usuario """
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users:login')
    
    def get_form_kwargs(self):
        """ Modifica los kwarg (argumentos pasados al formulario) o contexto """
        kwargs = super(VerificationView,self).get_form_kwargs()
        kwargs.update({ 'pk' : self.kwargs['pk'] })
        return kwargs
    
    def form_valid(self, form): 
        """" Actualizamos el atributo 'is_active', una vez que se valida la información """
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )
        
        return super(VerificationView, self).form_valid(form)
    
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

    
class PasswordUpdateView(LoginRequiredMixin, FormView):
    """ Vista para realizar el cambio de password """
    template_name = 'users/password_update.html'
    form_class = PasswordUpdateForm
    success_url = reverse_lazy('users:login')
    login_url = reverse_lazy('users:login')
        
    user_log = {}
    
    def get_form_kwargs(self):
        """ Modifica los kwarg (argumentos pasados al formulario) o contexto """
        self.user_log=self.request.user # Recuperar el usuario activo
        kwargs = super(PasswordUpdateView,self).get_form_kwargs()
        kwargs.update({ 'username' : self.user_log.username })
        return kwargs
    
    def form_valid(self, form):
        """ Modifica el password del usuario """
        new_password = form.cleaned_data['password2']
        self.user_log.set_password(new_password)
        self.user_log.save()
        logout(self.request)        
        return super(PasswordUpdateView, self).form_valid(form)
        
        