# inventario/urls.py
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('agregar/', views.agregar_producto, name='agregar_producto'), #muestra la vista de agregar un producto
    path('cuadre/', views.registrar_cuadre_caja, name='cuadre_caja'), # muestra la vista del cuadre de caja
    path('lista/', views.lista_productos, name='lista_productos'), # MUESTRA LA VISTA DEL INVENTARIO
    path('api/total_ventas/', views.total_ventas_por_dia, name='total_ventas_por_dia'),




]


