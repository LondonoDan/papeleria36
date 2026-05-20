from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import LoginForm, CrearUsuarioForm, EditarUsuarioForm
from .models import Perfil


# ── Login ──
def login_view(request):
    # Si ya está autenticado, ir al inicio
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if usuario:
            login(request, usuario)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'usuarios/login.html', {'form': form})


# ── Logout ──
def logout_view(request):
    logout(request)
    return redirect('usuarios:login')


# ── Lista de usuarios (solo administrador) ──
@login_required
def lista_usuarios(request):
    if not request.user.perfil.es_administrador():
        messages.error(request, 'No tienes permiso para acceder a esta sección.')
        return redirect('home')

    usuarios = User.objects.all().select_related('perfil')
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


# ── Crear usuario (solo administrador) ──
@login_required
def crear_usuario(request):
    if not request.user.perfil.es_administrador():
        messages.error(request, 'No tienes permiso para acceder a esta sección.')
        return redirect('home')

    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Perfil.objects.create(
                usuario=usuario,
                rol=form.cleaned_data['rol']
            )
            messages.success(request, f"Usuario '{usuario.username}' creado correctamente.")
            return redirect('usuarios:lista_usuarios')
    else:
        form = CrearUsuarioForm()

    return render(request, 'usuarios/crear_usuario.html', {'form': form})


# ── Editar usuario (solo administrador) ──
@login_required
def editar_usuario(request, pk):
    if not request.user.perfil.es_administrador():
        messages.error(request, 'No tienes permiso para acceder a esta sección.')
        return redirect('home')

    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            usuario.perfil.rol = form.cleaned_data['rol']
            usuario.perfil.save()
            messages.success(request, f"Usuario '{usuario.username}' actualizado.")
            return redirect('usuarios:lista_usuarios')
    else:
        form = EditarUsuarioForm(instance=usuario)

    return render(request, 'usuarios/editar_usuario.html', {
        'form': form,
        'usuario': usuario,
    })


# ── Eliminar usuario (solo administrador) ──
@login_required
def eliminar_usuario(request, pk):
    if not request.user.perfil.es_administrador():
        messages.error(request, 'No tienes permiso para acceder a esta sección.')
        return redirect('home')

    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        nombre = usuario.username
        usuario.delete()
        messages.success(request, f"Usuario '{nombre}' eliminado.")
        return redirect('usuarios:lista_usuarios')

    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})