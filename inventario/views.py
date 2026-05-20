# inventario/views.py
from django.shortcuts import render, redirect
from .forms import ProductoForm
from django.contrib import messages
from .forms import CuadreCajaForm
from .models import Producto
from django.http import JsonResponse
from ventas.models import Venta
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required



#agregando producto
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el producto en la base de datos
            # Redirige a una vista de listado o a una página de éxito
            messages.success(request, "Producto guardado correctamente.")  # Asegúrate de definir esta URL o cámbiala
            return redirect('inventario:lista_productos')
    # Opcional: limpiar el formulario para que no se muestre la data anterior
        form = ProductoForm()
    else:
        form = ProductoForm()

    return render(request, 'inventario/agregar_producto.html', {'form': form})

#LISTADO DE PRODUCTOS REGISTRADOS
def lista_productos(request):
    productos = Producto.objects.all()  # Recupera todos los productos
    return render(request, 'inventario/lista_productos.html', {'productos': productos})

@login_required
def editar_producto(request, pk):
    if request.user.perfil.rol != 'administrador':
        messages.error(request, 'Solo los administradores pueden editar productos.')
        return redirect('inventario:lista_productos')

    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f"Producto '{producto.nombre}' actualizado correctamente.")
            return redirect('inventario:lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/editar_producto.html', {
        'form': form,
        'producto': producto,
    })

@login_required
def eliminar_producto(request, pk):
    if request.user.perfil.rol != 'administrador':
        messages.error(request, 'Solo los administradores pueden eliminar productos.')
        return redirect('inventario:lista_productos')

    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f"Producto '{nombre}' eliminado correctamente.")
        return redirect('inventario:lista_productos')
    return render(request, 'inventario/eliminar_producto.html', {'producto': producto})























#CUADRE DE CAJA
def registrar_cuadre_caja(request):
    if request.method == 'POST':
        form = CuadreCajaForm(request.POST)
        if form.is_valid():
            cuadre = form.save()  # Esto ejecuta el save() del modelo y hace los cálculos
            messages.success(request, f"Cuadre guardado. Valor a entregar: {cuadre.valor_entregar}")
            # Puedes redirigir a una vista de listado o a la misma página para ingresar otro
            return redirect('inventario:cuadre_caj')  # redirige a el mismo cuadre de caja con un mensaje
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = CuadreCajaForm()
    return render(request, 'inventario/cuadre_caja.html', {'form': form})
