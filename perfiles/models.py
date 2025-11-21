from django.db import models
from django.contrib.auth.models import User

class Curso(models.Model):
    nombre_colegio = models.CharField(max_length=100, default='Colegio Ejemplo')
    nombre_curso = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre_curso} - {self.nombre_colegio}'

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='alumnos')

    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    ROL_CHOICES = (
        ('presidente', 'Presidente'),
        ('tesorero', 'Tesorero'),
        ('apoderado', 'Apoderado'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    alumno = models.ForeignKey(Alumno, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.get_rol_display()}'