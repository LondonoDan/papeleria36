# ventas/forms.py
from django import forms
from django_select2.forms import ModelSelect2Widget
from inventario.models import Producto
from django.forms import inlineformset_factory
from .models import Venta, DetalleVenta

#FORMULARIO VENTAS
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['total', 'metodo_pago', 'descuento', 'descripcion_descuento']
        # Nota: el campo 'fecha' lo generamos automáticamente con auto_now_add en el modelo.

# Formulario personalizado para DetalleVenta
class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio']
        widgets = {
            'producto': ModelSelect2Widget(
                model=Producto,
                search_fields=['nombre__icontains'],
                queryset=Producto.objects.filter(nombre__icontains='a')  # solo para probar
            )
        }



# Creamos un inline formset para DetalleVenta asociado a Venta.
DetalleVentaFormSet = inlineformset_factory(
    parent_model=Venta,
    model=DetalleVenta,
    fields=('producto', 'cantidad', 'precio'),
    extra=1,   # Número de formularios extra para agregar detalles
    can_delete=True
)

#Vista ventas 
class FiltroDiaForm(forms.Form):
    dia = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Filtrar por día"
    )