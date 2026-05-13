from django.db import models


# clase productos con sus campos
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre,self.precio
    

# Clase cuadre de caja con sus campos
class CuadreCaja(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    dia_cuadre = models.DateField(null=True, blank=True)  # Agregado
    billetes_100mil = models.IntegerField(default=0)
    billetes_50mil = models.IntegerField(default=0)
    billetes_20mil = models.IntegerField(default=0)
    billetes_10mil = models.IntegerField(default=0)
    billetes_5mil = models.IntegerField(default=0)
    billetes_2mil = models.IntegerField(default=0)
    billetes_1mil = models.IntegerField(default=0)
    monedas_500 = models.IntegerField(default=0)
    monedas_200 = models.IntegerField(default=0)
    monedas_100 = models.IntegerField(default=0)
    monedas_50 = models.IntegerField(default=0)
    total_efectivo = models.DecimalField(max_digits=10, decimal_places=2)
    base_caja = models.DecimalField(max_digits=10, decimal_places=2, default=150000)
    valor_qr = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nomina = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_entregar = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # 1. Calcular total de ventas del día
        if self.dia_cuadre:
            self.total_ventas = (Venta.objects
                                 .filter(fecha__date=self.dia_cuadre)
                                 .aggregate(total=Sum('total'))['total'] or 0)

        # 2. Sumar todos los billetes y monedas para calcular total_efectivo
        sum_billetes = (
            self.billetes_100mil * 100000 +
            self.billetes_50mil  * 50000  +
            self.billetes_20mil  * 20000  +
            self.billetes_10mil  * 10000  +
            self.billetes_5mil   * 5000   +
            self.billetes_2mil   * 2000   +
            self.billetes_1mil   * 1000
        )
        sum_monedas = (
            self.monedas_500 * 500 +
            self.monedas_200 * 200 +
            self.monedas_100 * 100 +
            self.monedas_50  * 50
        )
        self.total_efectivo = sum_billetes + sum_monedas

        # 3. Calcular valor a entregar
        #    valor_entregar = total_efectivo - base_caja - valor_qr - nomina
        self.valor_entregar = self.total_efectivo - self.base_caja - self.valor_qr - self.nomina

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cuadre de {self.dia_cuadre or self.fecha.date()} - Total: {self.total_efectivo}"


    
        