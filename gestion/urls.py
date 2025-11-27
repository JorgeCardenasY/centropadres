from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('ajax/get-alumnos-for-apoderado/', views.get_alumnos_for_apoderado, name='get_alumnos_for_apoderado'),
    path('conceptos/', views.ConceptoListView.as_view(), name='gestion_conceptos'),
    path('conceptos/nuevo/', views.ConceptoCreateView.as_view(), name='concepto_create'),
    path('conceptos/<int:pk>/editar/', views.ConceptoUpdateView.as_view(), name='concepto_update'),
    path('conceptos/<int:pk>/eliminar/', views.ConceptoDeleteView.as_view(), name='concepto_delete'),
    path('asignar-concepto/', views.assign_concept_to_apoderado, name='assign_concept'),
    path('reporte/', views.reporte_curso, name='reporte_curso'),
    path('registrar-pago/', views.registrar_pago_view, name='registrar_pago'),
    path('pagos/', views.RegistroPagoListView.as_view(), name='manage_pagos'),
    path('pagos/<int:pk>/editar/', views.RegistroPagoUpdateView.as_view(), name='edit_pago'),
    path('pagos/<int:pk>/eliminar/', views.RegistroPagoDeleteView.as_view(), name='delete_pago'),
]