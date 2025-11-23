from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('ajax/get-alumnos-for-apoderado/', views.get_alumnos_for_apoderado, name='get_alumnos_for_apoderado'),
]