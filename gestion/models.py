from django.db import models
from perfiles.models import Apoderado, Alumno

class Concepto(models.Model):
    concepto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    descriptor = models.CharField(max_length=500)
    numero_cuotas = models.IntegerField()
    fecha_limite = models.DateField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nombre

class Deuda(models.Model):
    deuda_id = models.AutoField(primary_key=True)
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE, related_name='deudas')
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='deudas')
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE, related_name='deudas')
    pagada = models.BooleanField(default=False)

    def __str__(self):
        return f'Deuda de {self.apoderado} por {self.concepto} para {self.alumno}'

class RegistroPago(models.Model):
    METODO_PAGO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('TARJETA', 'Tarjeta'),
        ('OTRO', 'Otro'),
    ]
    
    deuda = models.ForeignKey(Deuda, on_delete=models.CASCADE, related_name='pagos', null=True)
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE, related_name='pagos_realizados')
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='pagos_recibidos')
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE, related_name='pagos')
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    fecha = models.DateField(auto_now_add=True)
    registrador = models.ForeignKey(
        Apoderado, 
        on_delete=models.SET_NULL, 
        related_name='pagos_registrados', 
        null=True
    )

    def __str__(self):
        return f'Pago de {self.monto_pagado} por {self.alumno} para {self.concepto}'
