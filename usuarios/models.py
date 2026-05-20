from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    ROL_CHOICES = [
        ('administrador', 'Administrador'),
        ('vendedor', 'Vendedor'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='vendedor')

    def es_administrador(self):
        return self.rol == 'administrador'

    def es_vendedor(self):
        return self.rol == 'vendedor'

    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"