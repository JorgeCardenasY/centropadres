from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from .models import Pago, Concepto
from .forms import PagoForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ConceptoListView(LoginRequiredMixin, ListView):
    model = Concepto
    template_name = 'gestion/concepto_list.html'
    context_object_name = 'conceptos'

class ConceptoDetailView(LoginRequiredMixin, DetailView):
    model = Concepto
    template_name = 'gestion/concepto_detail.html'
    context_object_name = 'concepto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagos_realizados'] = Pago.objects.filter(
            apoderado=self.request.user,
            concepto=self.object
        )
        return context

class PagoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Pago
    form_class = PagoForm
    template_name = 'gestion/pago_form.html'
    success_url = reverse_lazy('pago-list')

    def form_valid(self, form):
        form.instance.registrado_por = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.perfil.rol == 'tesorero'

class PagoListView(LoginRequiredMixin, ListView):
    model = Pago
    template_name = 'gestion/pago_list.html'
    context_object_name = 'pagos'

    def get_queryset(self):
        if self.request.user.perfil.rol == 'tesorero':
            return Pago.objects.all()
        return Pago.objects.filter(apoderado=self.request.user)