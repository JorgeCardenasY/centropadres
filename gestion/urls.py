from django.urls import path
from . import views

urlpatterns = [
    path('ajax/get-alumnos-for-apoderado/', views.get_alumnos_for_apoderado, name='ajax_get_alumnos_for_apoderado'),
]
