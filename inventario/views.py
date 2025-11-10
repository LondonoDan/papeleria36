# inventario/views.py
from django.shortcuts import render, redirect
from .forms import ProductoForm
from django.contrib import messages
from .forms import CuadreCajaForm
from .models import Producto
from django.http import JsonResponse
from ventas.models import Venta
from django.db.models import Sum


#Muestra el total de ventas por día escogido
def total_ventas_por_dia(request):
    """Retorna el total de ventas para la fecha dada en ?dia=YYYY-MM-DD"""
    dia = request.GET.get('dia')  # '2025-02-26'
    if not dia:
        return JsonResponse({'total_ventas': 0})
    
    total = (Venta.objects
             .filter(fecha__date=dia)
             .aggregate(suma=Sum('total'))['suma'] or 0)
    return JsonResponse({'total_ventas': float(total)})



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
