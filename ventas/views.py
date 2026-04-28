# ventas/VISTA de ventas.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import VentaForm, DetalleVentaFormSet
from .forms import FiltroDiaForm  # <-- Importa tu formulario
from django.http import JsonResponse
from django.db.models import Sum
from .models import Venta,DetalleVenta
from django.http import JsonResponse 
from inventario.models import Producto

def total_ventas_por_dia(request):
    """
    Retorna el total de ventas para la fecha dada en formato JSON.
    Ejemplo: /ventas/api/total_ventas/?dia=2025-02-28
    """
    dia = request.GET.get('dia')
    if not dia:
        return JsonResponse({'total_ventas': 0})
    total = (Venta.objects
             .filter(fecha__date=dia)
             .aggregate(suma=Sum('total'))['suma'] or 0)
    return JsonResponse({'total_ventas': float(total)})



#Registro de venta

def registrar_venta(request):
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        formset = DetalleVentaFormSet(request.POST)
        if venta_form.is_valid() and formset.is_valid():
            venta = venta_form.save()  # Guarda la venta
            formset.instance = venta   # Asigna la venta a cada formulario del formset
            formset.save()             # Guarda todos los detalles
            messages.success(request, "Venta registrada correctamente.")
            return redirect('ventas:registrar_venta')  # Redirige a la vista de registrar una venta con un mensaje
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        venta_form = VentaForm()
        formset = DetalleVentaFormSet()
    
    context = {
        'venta_form': venta_form,
        'formset': formset,
    }
    return render(request, 'ventas/registrar_venta.html', context)



def total_ventas_qr_por_dia(request):
    """
    Retorna el total de ventas realizadas con método de pago 'QR' para la fecha dada en formato JSON.
    Ejemplo: /ventas/api/total_ventas_qr/?dia=2025-02-28
    """
    dia = request.GET.get('dia')
    if not dia:
        return JsonResponse({'total_ventas_qr': 0})
    
    total = (Venta.objects
             .filter(fecha__date=dia, metodo_pago='QR')
             .aggregate(suma=Sum('total'))['suma'] or 0)
    
    return JsonResponse({'total_ventas_qr': float(total)})

#filtra ventas realizadas por día
def reporte_ventas(request):
    form = FiltroDiaForm(request.GET or None)
    detalles = []

    if form.is_valid():
        dia = form.cleaned_data.get('dia')
        if dia:
            # Filtra los detalles de venta cuyo día coincida con la fecha de la venta
            detalles = DetalleVenta.objects.filter(venta__fecha__date=dia)
        else:
            # Si no se elige fecha, puedes mostrar todos o ninguno, tú decides
            detalles = DetalleVenta.objects.all()

    return render(request, 'ventas/reporte_ventas.html', {
        'form': form,
        'detalles': detalles
    })
    
    
    #trae el precio del prducto
def get_precio_producto(request): 
    producto_id = request.GET.get('id') 
    try: 
        producto = Producto.objects.get(id=producto_id) 
        return JsonResponse({'precio': float(producto.precio)}) 
    except Producto.DoesNotExist: 
        return JsonResponse({'precio': 0})
