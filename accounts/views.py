from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login feito com sucesso.')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')


def cadastro_1(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro_1.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha_2 = request.POST.get('senha_2')

    if not nome or not sobrenome or not email or not usuario or not senha or not senha_2:
        messages.error(request, 'Nenhum campo pode ficar vazio.')
        return render(request, 'accounts/cadastro_1.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido.')
        return render(request, 'accounts/cadastro_1.html')

    if len(senha) < 8:
        messages.error(request, 'O usuário precisa ter, no mínimo, 6 caracteres.')
        return render(request, 'accounts/cadastro_1.html')

    if len(senha) < 8:
        messages.error(request, 'A senha precisa ter, no mínimo, 8 caracteres.')
        return render(request, 'accounts/cadastro_1.html')

    if senha != senha_2:
        messages.error(request, 'As senhas são diferentes.')
        return render(request, 'accounts/cadastro_1.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já cadastrado.')
        return render(request, 'accounts/cadastro_1.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email de usuário já cadastrado.')
        return render(request, 'accounts/cadastro_1.html')

    messages.success(request, 'Usuário registrado!')
    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao enviar.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} salvo com sucesso.')
    return redirect('dashboard')
