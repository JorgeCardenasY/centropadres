from django.db import models
from django.contrib.auth.models import User

class Persona(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    rut_dni = models.CharField(max_length=20, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

class Apoderado(Persona):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='apoderado', null=True, blank=True)
    apoderado_id = models.AutoField(primary_key=True)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    registrar_pago = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

class Alumno(Persona):
    alumno_id = models.AutoField(primary_key=True)
    curso = models.CharField(max_length=100)
    colegio = models.CharField(max_length=100)
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE, related_name='alumnos')

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'
