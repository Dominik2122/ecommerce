from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model

from .forms import LoginForm, RegisterForm


User = get_user_model()

def home_page(request):
    return render(request,'index.html', {})

def login_page(request):
    login_form = LoginForm(request.POST or None)
    context = {'form': login_form}
    if login_form.is_valid():

        user = authenticate(request, username = login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
        print(login_form.cleaned_data['username'], login_form.cleaned_data['password'], user)
        if user is not None:
            login(request,user)
            context['form'] = LoginForm()
            return redirect('index')
        else:
            return HttpResponse('error')

    return render(request,'login.html', context)

def register_page(request):
    register_form = RegisterForm(request.POST or None)
    context = {'form': register_form}
    if register_form.is_valid():
        username = register_form.cleaned_data['username']
        password = register_form.cleaned_data['password']
        password2 = register_form.cleaned_data['password2']
        email= register_form.cleaned_data['email']
        new_user = User.objects.create_user(username, email)
        new_user.save()
        new_user.set_password(password)
        new_user.save()
        login(request,new_user)
        return redirect('index')


    return render(request,'register.html', context)
