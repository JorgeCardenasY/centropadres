from django.http import JsonResponse
from perfiles.models import Apoderado, Alumno
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Sum

from .models import Concepto, Deuda, RegistroPago
from .forms import ConceptoForm, AssignConceptForm, RegistroPagoForm

def registrador_required(function=None, redirect_field_name=None, login_url='login'):
    """
    Decorator for views that checks that the user is logged in and is a registrador,
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, 'apoderado') and u.apoderado.registrar_pago,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

@registrador_required
def registrar_pago_view(request):
    if request.method == 'POST':
        form = RegistroPagoForm(request.POST)
        if form.is_valid():
            registro_pago = form.save(commit=False)
            registro_pago.registrador = request.user.apoderado
            
            # Find the corresponding Deuda object
            try:
                deuda = Deuda.objects.get(
                    apoderado=registro_pago.apoderado,
                    alumno=registro_pago.alumno,
                    concepto=registro_pago.concepto
                )
                registro_pago.deuda = deuda
            except Deuda.DoesNotExist:
                messages.error(request, "No se encontró una deuda correspondiente para este pago.")
                return render(request, 'gestion/registrar_pago.html', {'form': form, 'title': 'Registrar Pago'})

            registro_pago.save()
            messages.success(request, "Pago registrado exitosamente.")
            return redirect('gestion:registrar_pago')
    else:
        form = RegistroPagoForm()

    context = {
        'form': form,
        'title': 'Registrar Pago'
    }
    return render(request, 'gestion/registrar_pago.html', context)

@registrador_required
def reporte_curso(request):
    conceptos = Concepto.objects.all()
    selected_concepto_id = request.GET.get('concepto')
    
    deudas = Deuda.objects.all().select_related('apoderado', 'alumno', 'concepto')
    
    if selected_concepto_id:
        deudas = deudas.filter(concepto_id=selected_concepto_id)
        
    report_data = []
    for deuda in deudas:
        pagado = RegistroPago.objects.filter(deuda=deuda).aggregate(total=Sum('monto_pagado'))['total'] or 0
        adeudado = deuda.concepto.monto_total - pagado
        report_data.append({
            'apoderado': deuda.apoderado,
            'alumno': deuda.alumno,
            'concepto': deuda.concepto,
            'monto_a_pagar': deuda.concepto.monto_total,
            'pagado': pagado,
            'monto_adeudado': adeudado,
        })
        
    context = {
        'report_data': report_data,
        'conceptos': conceptos,
        'selected_concepto_id': selected_concepto_id,
        'title': 'Reporte General del Curso'
    }
    return render(request, 'gestion/reporte_curso.html', context)

def get_alumnos_for_apoderado(request):
    apoderado_id = request.GET.get('apoderado_id')
    if apoderado_id:
        try:
            apoderado = Apoderado.objects.get(pk=apoderado_id)
            alumnos = apoderado.alumnos.all().values('alumno_id', 'nombres', 'apellidos')
            return JsonResponse({'alumnos': list(alumnos)})
        except Apoderado.DoesNotExist:
            return JsonResponse({'alumnos': []})
    return JsonResponse({'alumnos': []})

@registrador_required
def assign_concept_to_apoderado(request):
    if request.method == 'POST':
        form = AssignConceptForm(request.POST)
        if form.is_valid():
            apoderado = form.cleaned_data['apoderado']
            concepto = form.cleaned_data['concepto']

            # Create Deuda instances for all Alumnos associated with the selected Apoderado
            alumnos = apoderado.alumnos.all()
            if not alumnos:
                messages.warning(request, f"El apoderado {apoderado.nombres} {apoderado.apellidos} no tiene alumnos asociados. No se asignó ninguna deuda.")
                return redirect('gestion:assign_concept')

            deudas_creadas = 0
            for alumno in alumnos:
                Deuda.objects.get_or_create(
                    apoderado=apoderado,
                    alumno=alumno,
                    concepto=concepto
                )
                deudas_creadas += 1
            
            messages.success(request, f"Concepto '{concepto.nombre}' asignado a {deudas_creadas} alumno(s) de {apoderado.nombres} {apoderado.apellidos}.")
            return redirect('gestion:assign_concept')
    else:
        form = AssignConceptForm()
    
    context = {
        'form': form,
        'title': 'Asignar Concepto de Pago a Apoderado'
    }
    return render(request, 'gestion/assign_concept.html', context)


@method_decorator(login_required, name='dispatch')
class ConceptoListView(ListView):
    model = Concepto
    template_name = 'gestion/concepto_list.html'
    context_object_name = 'conceptos'

@method_decorator(login_required, name='dispatch')
class ConceptoCreateView(CreateView):
    model = Concepto
    form_class = ConceptoForm
    template_name = 'gestion/concepto_form.html'
    success_url = reverse_lazy('gestion:gestion_conceptos')

@method_decorator(login_required, name='dispatch')
class ConceptoUpdateView(UpdateView):
    model = Concepto
    form_class = ConceptoForm
    template_name = 'gestion/concepto_form.html'
    success_url = reverse_lazy('gestion:gestion_conceptos')

@method_decorator(login_required, name='dispatch')
class ConceptoDeleteView(DeleteView):
    model = Concepto
    template_name = 'gestion/concepto_confirm_delete.html'
    success_url = reverse_lazy('gestion:gestion_conceptos')
