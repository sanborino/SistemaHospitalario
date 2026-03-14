from acceso.models import UsuarioRol

def roles_usuario(request):
    if not request.user.is_authenticated:
        return {"roles_usuario": []}

    roles = UsuarioRol.objects.filter(usuario=request.user).select_related("rol")

    return {
        "roles_usuario": [r.rol.nombre for r in roles]
    }
