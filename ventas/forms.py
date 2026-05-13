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
 
        )
    }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['precio'].required = False
        self.fields['precio'].widget.attrs['readonly'] = True

    # Solo asignar precio si la instancia tiene producto
        if getattr(self.instance, "producto", None):
            self.fields['precio'].initial = self.instance.producto.precio


# Creamos un inline formset para DetalleVenta asociado a Venta.
DetalleVentaFormSet = inlineformset_factory(
    parent_model=Venta,
    model=DetalleVenta,
    form=DetalleVentaForm,   # usamos el form personalizado
    fields=('producto', 'cantidad', 'precio'),
    extra=1,   # al menos un formulario inicial
    can_delete=True
)


#Vista ventas - esto esta
class FiltroDiaForm(forms.Form):
    dia = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Filtrar por día"
    )