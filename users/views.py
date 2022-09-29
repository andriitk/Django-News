from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, LoginUserForm
from django.contrib.auth.views import LoginView


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class Login(LoginView):
    authentication_form = LoginUserForm
    template_name = 'registration/login.html'
    form_class = LoginUserForm
