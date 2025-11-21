from django.db import models
from django.contrib.auth.models import User

class Concepto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad_cuotas = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre

class Pago(models.Model):
    apoderado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pagos_realizados')
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pagos_registrados')

    def __str__(self):
        return f'Pago de {self.apoderado.username} por {self.concepto.nombre} - ${self.monto}'


class Apoderado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    metodo_pago_preferido = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Cuota(models.Model):
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE)
    numero_cuota = models.IntegerField()
    monto_cuota = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Cuota {self.numero_cuota} de {self.concepto.nombre} - ${self.monto_cuota}'

class Estudiante(models.Model):
    Estudiante = models.OneToOneField(User, on_delete=models.CASCADE)
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE, related_name='estudiantes')
    grado = models.CharField(max_length=50)
    colegio = models.CharField(max_length=100)

    def __str__(self):
        return self.Estudiante.username