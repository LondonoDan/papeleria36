# ventas/urls.py
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('registrar/', views.registrar_venta, name='registrar_venta'),
    # Puedes definir una vista de listado para ventas, por ejemplo:
    # path('lista/', views.lista_ventas, name='lista_ventas'),
    #path('api/total_ventas/', views.total_ventas_por_dia, name='total_ventas_por_dia'),
    #path('api/total_ventas_qr/', views.total_ventas_qr_por_dia, name='total_ventas_qr_por_dia'),
    path('reporte/', views.reporte_ventas, name='reporte_ventas'),
    path('api/get_precio_producto/', views.get_precio_producto, name='get_precio_producto'),
    
]
