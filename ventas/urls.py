# ventas/urls.py
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('registrar/', views.registrar_venta, name='registrar_venta'),
    path('reporte/', views.reporte_por_dia, name='reporte_ventas'),
    path('api/get_precio_producto/', views.get_precio_producto, name='get_precio_producto'),
    path('api/listar_productos/',     views.listar_productos,      name='listar_productos'),  # ← NUEVO
]
