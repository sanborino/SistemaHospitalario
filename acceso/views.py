from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UsuarioForm
from acceso.models import UsuarioRol

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('hospital:hospital')
    
    return render(request, 'index.html', {
        'title': 'Bienvenido Sistema Hospitalario'
    })
    
def registro(request):
    
    if request.user.is_authenticated:
        return redirect('hospital:hospital')

    else:
    
        register_form = UsuarioForm()
        
        
        if request.method == 'POST':
            register_form = UsuarioForm(request.POST)
            
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Te has registrado correctamente!!')
                
                return redirect('hospital:hospital')
        
        return render(request, 'registro.html',{
            'title': 'Registro',
            'register_form': register_form
        })
    
def login_usuario(request):
    
    if request.user.is_authenticated:
        return redirect('hospital:hospital')
    else:
    
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                roles = UsuarioRol.objects.filter(usuario=user).select_related("rol")
                roles_normalizados = [r.rol.nombre.strip().upper() for r in roles]
                request.session["roles_usuario"] = roles_normalizados

                return redirect('hospital:hospital')
            else:
                messages.warning(request, 'No te has identificado correctamente :(')
        
        return render(request, 'login.html' ,{
            'title': 'Identificate'
        })
    
def logout_usuario(request):
    logout(request)
    return redirect('index')

