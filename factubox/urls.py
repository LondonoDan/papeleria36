from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.urls import include, path
from django.shortcuts import render


def home(request):
    return render(request, 'home.html') # Renderiza la plantilla de inicio
    


# Aquí se incluyen las rutas de la app
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Página principal  # Esto hace que la página principal muestre un mensaje
    path('inventario/', include('inventario.urls')),  
    path('ventas/', include('ventas.urls')),
    path('select2/', include('django_select2.urls')),  # Agrega esta línea
    

]


