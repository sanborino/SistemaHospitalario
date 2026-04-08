from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import (
    UsuarioForm,
    RolForm,
    PermisoForm,
    UsuarioRolForm,
    RolPermisoForm,
    UsuarioHospitalForm,
)
from .models import Usuario, Rol, Permiso, UsuarioRol, RolPermiso, UsuarioHospital
from acceso.mixins import permiso_alto_required


@login_required
def index(request):
    usuario = request.user

    # Si el usuario está autenticado, obtenemos sus roles
    roles_usuario = list(
        UsuarioRol.objects.filter(usuario=usuario).values_list("rol__nombre", flat=True)
    )

    # Si quieres que al entrar se redirija a hospitales directamente:
    if usuario.is_authenticated:
        return redirect("acceso:hospitales")

    # Si no está autenticado, mostramos la página de inicio
    return render(
        request,
        "acceso/index.html",
        {
            "title": "Bienvenido Sistema Hospitalario",
            "roles_usuario": roles_usuario,
        },
    )


def registro(request):

    if request.user.is_authenticated:
        return redirect("acceso:hospitales")

    else:

        register_form = UsuarioForm()

        if request.method == "POST":
            register_form = UsuarioForm(request.POST)

            if register_form.is_valid():
                register_form.save()
                messages.success(request, "Te has registrado correctamente!!")

                return redirect("acceso:hospitales")

        return render(
            request,
            "acceso/registro.html",
            {"title": "Registro", "register_form": register_form},
        )


def login_usuario(request):

    if request.user.is_authenticated:
        return redirect("acceso:hospitales")
    else:

        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                roles = UsuarioRol.objects.filter(usuario=user).select_related("rol")
                roles_normalizados = [r.rol.nombre.strip().upper() for r in roles]
                request.session["roles_usuario"] = roles_normalizados

                return redirect("acceso:hospitales")
            else:
                messages.warning(request, "No te has identificado correctamente :(")

        return render(request, "acceso/login.html", {"title": "Identificate"})


def logout_usuario(request):
    logout(request)
    return redirect("acceso:index")


# CRUD Usuario
@permiso_alto_required
def usuario_lista(request):
    usuarios = Usuario.objects.all()
    return render(request, "acceso/usuario_lista.html", {"usuarios": usuarios})


@permiso_alto_required
def usuario_crear(request):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Usuario creado correctamente.")
        return redirect("acceso:usuario_lista")
    return render(
        request, "acceso/usuario_form.html", {"form": form, "titulo": "Crear Usuario"}
    )


@permiso_alto_required
def usuario_editar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form = UsuarioForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect("acceso:usuario_lista")
    return render(
        request, "acceso/usuario_form.html", {"form": form, "titulo": "Editar Usuario"}
    )


@permiso_alto_required
def usuario_eliminar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == "POST":
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect("acceso:usuario_lista")
    return render(
        request, "acceso/usuario_confirmar_eliminar.html", {"usuario": usuario}
    )


# CRUD Rol
@permiso_alto_required
def rol_lista(request):
    roles = Rol.objects.all()
    return render(request, "acceso/rol_lista.html", {"roles": roles})


@permiso_alto_required
def rol_crear(request):
    form = RolForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Rol creado correctamente.")
        return redirect("acceso:rol_lista")
    return render(
        request, "acceso/rol_form.html", {"form": form, "titulo": "Crear Rol"}
    )


@permiso_alto_required
def rol_editar(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    form = RolForm(request.POST or None, instance=rol)
    if form.is_valid():
        form.save()
        messages.success(request, "Rol actualizado correctamente.")
        return redirect("acceso:rol_lista")
    return render(
        request, "acceso/rol_form.html", {"form": form, "titulo": "Editar Rol"}
    )


@permiso_alto_required
def rol_eliminar(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    if request.method == "POST":
        rol.delete()
        messages.success(request, "Rol eliminado correctamente.")
        return redirect("acceso:rol_lista")
    return render(request, "acceso/rol_confirmar_eliminar.html", {"rol": rol})


# CRUD Permiso
@permiso_alto_required
def permiso_lista(request):
    permisos = Permiso.objects.all()
    return render(request, "acceso/permiso_lista.html", {"permisos": permisos})


@permiso_alto_required
def permiso_crear(request):
    form = PermisoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Permiso creado correctamente.")
        return redirect("acceso:permiso_lista")
    return render(
        request, "acceso/permiso_form.html", {"form": form, "titulo": "Crear Permiso"}
    )


@permiso_alto_required
def permiso_editar(request, pk):
    permiso = get_object_or_404(Permiso, pk=pk)
    form = PermisoForm(request.POST or None, instance=permiso)
    if form.is_valid():
        form.save()
        messages.success(request, "Permiso actualizado correctamente.")
        return redirect("acceso:permiso_lista")
    return render(
        request, "acceso/permiso_form.html", {"form": form, "titulo": "Editar Permiso"}
    )


@permiso_alto_required
def permiso_eliminar(request, pk):
    permiso = get_object_or_404(Permiso, pk=pk)
    if request.method == "POST":
        permiso.delete()
        messages.success(request, "Permiso eliminado correctamente.")
        return redirect("acceso:permiso_lista")
    return render(
        request, "acceso/permiso_confirmar_eliminar.html", {"permiso": permiso}
    )


# Asignar Rol a Usuario
@permiso_alto_required
def asignar_rol_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == "POST":
        form = UsuarioRolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rol asignado correctamente.")
            return redirect("acceso:usuario_detalle", pk=usuario_id)
    else:
        form = UsuarioRolForm(initial={"usuario": usuario})
    return render(
        request, "acceso/asignar_rol.html", {"form": form, "usuario": usuario}
    )


@permiso_alto_required
def quitar_rol_usuario(request, usuario_id, rol_id):
    usuario_rol = get_object_or_404(UsuarioRol, usuario_id=usuario_id, rol_id=rol_id)
    usuario_rol.delete()
    messages.success(request, "Rol quitado correctamente.")
    return redirect("acceso:usuario_detalle", pk=usuario_id)


# Asignar Permiso a Rol
@permiso_alto_required
def asignar_permiso_rol(request, rol_id):
    rol = get_object_or_404(Rol, pk=rol_id)

    if request.method == "POST":
        form = RolPermisoForm(request.POST)
        if form.is_valid():
            rp = form.save(commit=False)
            rp.rol = rol
            rp.save()
            messages.success(request, "Permiso asignado correctamente.")
            return redirect("acceso:rol_detalle", pk=rol_id)
    else:
        form = RolPermisoForm(initial={"rol": rol})

    return render(
        request,
        "acceso/asignar_permiso.html",
        {"form": form, "rol": rol},
    )


@permiso_alto_required
def quitar_permiso_rol(request, rol_id, permiso_id):
    rol_permiso = get_object_or_404(RolPermiso, rol_id=rol_id, permiso_id=permiso_id)
    rol_permiso.delete()
    messages.success(request, "Permiso quitado correctamente.")
    return redirect("acceso:rol_detalle", kwargs={"pk": rol_id})


# Detalles
@permiso_alto_required
def usuario_detalle(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    roles = UsuarioRol.objects.filter(usuario=usuario).select_related("rol")
    hospitales = UsuarioHospital.objects.filter(usuario=usuario).select_related(
        "hospital"
    )
    return render(
        request,
        "acceso/usuario_detalle.html",
        {"usuario": usuario, "roles": roles, "hospitales": hospitales},
    )


@permiso_alto_required
def rol_detalle(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    permisos = RolPermiso.objects.filter(rol=rol).select_related("permiso")
    usuarios = UsuarioRol.objects.filter(rol=rol).select_related("usuario")
    return render(
        request,
        "acceso/rol_detalle.html",
        {"rol": rol, "permisos": permisos, "usuarios": usuarios},
    )


@permiso_alto_required
def usuariohospital_list(request):
    registros = UsuarioHospital.objects.select_related("usuario", "hospital")
    return render(request, "acceso/list.html", {"registros": registros})


@permiso_alto_required
def usuariohospital_create(request):
    if request.method == "POST":
        form = UsuarioHospitalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado correctamente.")
            return redirect("acceso:usuariohospital_list")
    else:
        form = UsuarioHospitalForm()
    return render(request, "acceso/form.html", {"form": form})


@permiso_alto_required
def usuariohospital_update(request, pk):
    registro = get_object_or_404(UsuarioHospital, pk=pk)
    if request.method == "POST":
        form = UsuarioHospitalForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro actualizado correctamente.")
            return redirect("acceso:usuariohospital_list")
    else:
        form = UsuarioHospitalForm(instance=registro)
    return render(request, "acceso/form.html", {"form": form})


@permiso_alto_required
def usuariohospital_delete(request, pk):
    registro = get_object_or_404(UsuarioHospital, pk=pk)
    if request.method == "POST":
        registro.delete()
        messages.success(request, "Registro eliminado correctamente.")
        return redirect("usuariohospital_list")
    return render(request, "acceso/delete.html", {"registro": registro})


# Mantener vista antigua si es usada en otros lugares:
@login_required(login_url="login")
def hospital(request):
    roles_usuario = list(
        UsuarioRol.objects.filter(usuario=request.user).values_list(
            "rol__nombre", flat=True
        )
    )

    return render(request, "acceso/hospital.html", {"roles_usuario": roles_usuario})
