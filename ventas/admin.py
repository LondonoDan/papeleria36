from django.contrib import admin
from .models import Venta, DetalleVenta  # Importa solo los modelos de esta app

admin.site.register(Venta)
admin.site.register(DetalleVenta)


