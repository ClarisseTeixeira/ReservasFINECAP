from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate


def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password == password_confirm:
            try:
                user = User.objects.create_user(username=username, password=password)
                messages.success(request, 'Usuário registrado com sucesso.')
                return redirect('index')
            except:
                messages.error(request, 'Erro ao criar usuário.')
        else:
            messages.error(request, 'As senhas não coincidem.')


    return render(request, 'user/registro.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index') 
            
    else:
        form = AuthenticationForm()
    context = {'form': form}    
    return render(request, 'user/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')


def index(request):
    return render(request, "index.html")