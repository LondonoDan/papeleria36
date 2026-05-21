from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import VentaForm, DetalleVentaFormSet,DetalleVenta
from inventario.models import Producto
from .models import Venta
from .forms import FiltroDiaForm
from django.db import transaction
from decimal import Decimal
from django.contrib import messages  # ← para mensaje de error cuando el stock esta en 0


def registrar_venta(request):
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        formset = DetalleVentaFormSet(request.POST)

        if venta_form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    venta = venta_form.save(commit=False)
                    venta.total = 0
                    venta.save()

                    total = 0
                    detalles = formset.save(commit=False)

                    for detalle in detalles:
                        detalle.venta = venta

                        if detalle.producto:
                            detalle.precio = detalle.producto.precio
                            detalle.save()
                            total += detalle.subtotal()

                            # ── DESCONTAR STOCK ──
                            producto = detalle.producto
                            if producto.cantidad >= detalle.cantidad:
                                producto.cantidad -= detalle.cantidad
                                producto.save()
                            else:
                                raise ValueError(
                                    f"Stock insuficiente para '{producto.nombre}'. "
                                    f"Disponible: {producto.cantidad}, solicitado: {detalle.cantidad}."
                                )

                    # Aplicar descuento al total
                    descuento = venta.descuento or Decimal('0')
                    venta.total = total * (1 - descuento / Decimal('100'))
                    venta.save()

                return redirect('ventas:reporte_ventas')

            except ValueError as e:
                # Muestra el mensaje de error en el template sin página de error
                messages.error(request, str(e))

    else:
        venta_form = VentaForm()
        formset = DetalleVentaFormSet()

    return render(request, 'ventas/registrar_venta.html', {
        'venta_form': venta_form,
        'formset': formset,
    })


def get_precio_producto(request):
    """Devuelve el precio de un producto por su ID."""
    producto_id = request.GET.get('producto_id')
    try:
        producto = Producto.objects.get(id=producto_id)
        return JsonResponse({'precio': str(producto.precio)})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)


def listar_productos(request):
    """Devuelve lista de productos filtrados por nombre (para Select2 AJAX)."""
    q = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=q).values('id', 'nombre', 'precio')[:30]
    return JsonResponse({'productos': list(productos)})




# Filtro de venta por día escogido
def reporte_por_dia(request):
    form = FiltroDiaForm(request.GET or None)
    ventas = None
    dia = None

    if form.is_valid():
        dia = form.cleaned_data['dia']
        ventas = Venta.objects.filter(
            fecha__date=dia
        ).prefetch_related('detalleventa_set__producto').order_by('id')

    return render(request, 'ventas/reporte_ventas.html', {
        'form': form,
        'ventas': ventas,
        'dia': dia,
    })

