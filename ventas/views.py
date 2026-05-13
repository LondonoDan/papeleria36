from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import VentaForm, DetalleVentaFormSet,DetalleVenta
from inventario.models import Producto
from .models import Venta
from .forms import FiltroDiaForm

def registrar_venta(request):
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        formset = DetalleVentaFormSet(request.POST)

        if venta_form.is_valid() and formset.is_valid():
            venta = venta_form.save(commit=False)
            venta.save()

            detalles = formset.save(commit=False)
            for detalle in detalles:
                detalle.venta = venta
                if detalle.producto:   # ✅ solo si hay producto
                    detalle.precio = detalle.producto.precio
                detalle.save()


            # si tienes un método para calcular el total, lo llamas aquí
            # venta.calcular_total()
            return redirect('ventas:reporte_ventas')
    else:
        venta_form = VentaForm()
        formset = DetalleVentaFormSet()

    return render(request, 'ventas/registrar_venta.html', {
        'venta_form': venta_form,
        'formset': formset
    })



# AJAX para obtener precio del producto
def get_precio_producto(request):
    producto_id = request.GET.get('producto_id')
    try:
        producto = Producto.objects.get(id=producto_id)
        return JsonResponse({'precio': str(producto.precio)})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)






# Filtro de venta por día escogido
def reporte_ventas(request):
    form = FiltroDiaForm(request.GET)
    detalles = DetalleVenta.objects.all()

    if form.is_valid():
        dia = form.cleaned_data.get('dia')
        if dia:
            # Filtramos las ventas por fecha
            ventas = Venta.objects.filter(fecha__date=dia)
            # Filtramos los detalles asociados a esas ventas
            detalles = DetalleVenta.objects.filter(venta__in=ventas)

    return render(request, 'ventas/reporte_ventas.html', {
        'form': form,
        'detalles': detalles
    })

