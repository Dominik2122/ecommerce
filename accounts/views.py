from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import CreateView, FormView

from .forms import LoginForm, RegisterForm, GuestForm

User = get_user_model()
# Create your views here.


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login/'

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        user = authenticate(request, username = form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user is not None:
            login(request,user)
            if request.POST.get('checkout'):
                return redirect('carts:checkout')
            else:
                return redirect('index')
        else:
            return HttpResponse('error')
