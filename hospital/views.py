from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from acceso.models import UsuarioRol

# Create your views here.

@login_required(login_url="login")
def hospital(request):
    roles_usuario = list(
        UsuarioRol.objects.filter(usuario=request.user)
        .values_list('rol__nombre', flat=True)
    )

    return render(request, 'hospital.html', {
        'roles_usuario': roles_usuario
    })