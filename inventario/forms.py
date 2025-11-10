# inventario/forms.py
from django import forms
from .models import Producto
from .models import CuadreCaja

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'cantidad', 'descripcion']

# CUADRE DE CAJA

class CuadreCajaForm(forms.ModelForm):
    class Meta:
        model = CuadreCaja
        # Incluimos los campos que se deben ingresar.
        # Nota: Si 'fecha' y 'base_caja' tienen valores por defecto y no se ingresan manualmente, puedes omitirlos.
        fields = [
             # Campo de fecha para filtrar las ventas del día
            'billetes_100mil', 'billetes_50mil', 'billetes_20mil', 'billetes_10mil',
            'billetes_5mil', 'billetes_2mil', 'billetes_1mil', 'monedas_500',
            'monedas_200', 'monedas_100', 'monedas_50',
            'nomina', 
        ]
