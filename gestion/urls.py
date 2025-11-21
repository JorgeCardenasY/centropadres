from django.urls import path
from .views import PagoListView, PagoCreateView, ConceptoListView, ConceptoDetailView

urlpatterns = [
    path('', ConceptoListView.as_view(), name='concepto-list'),
    path('concepto/<int:pk>/', ConceptoDetailView.as_view(), name='concepto-detail'),
    path('pagos/', PagoListView.as_view(), name='pago-list'),
    path('pagos/registrar/', PagoCreateView.as_view(), name='pago-create'),
]
