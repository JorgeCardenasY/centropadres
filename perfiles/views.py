from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Perfil, Curso, Alumno
from django.contrib.auth.models import User
from .forms import UserCreationForm, PerfilForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class PerfilListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Perfil
    template_name = 'perfiles/perfil_list.html'
    context_object_name = 'perfiles'

class PerfilCreateView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'perfiles/perfil_form.html'
    success_url = reverse_lazy('perfil-list')

    def form_valid(self, form):
        user = form.save()
        # Manually create the profile because the form is complex
        Perfil.objects.create(user=user, rol=self.request.POST.get('rol', 'apoderado'))
        return super().form_valid(form)


class PerfilUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = Perfil
    form_class = PerfilForm
    template_name = 'perfiles/perfil_form.html'
    success_url = reverse_lazy('perfil-list')

class PerfilDeleteView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = Perfil
    template_name = 'perfiles/perfil_confirm_delete.html'
    success_url = reverse_lazy('perfil-list')

class PerfilesExplanationView(TemplateView):
    template_name = 'perfiles/perfiles.html'

@login_required
def mi_curso(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    alumno = perfil.alumno
    curso = alumno.curso if alumno else None

    if curso:
        presidente = Perfil.objects.filter(alumno__curso=curso, rol='presidente').first()
        apoderados = Perfil.objects.filter(alumno__curso=curso).select_related('user', 'alumno')
    else:
        presidente = None
        apoderados = []

    context = {
        'curso': curso,
        'presidente': presidente,
        'apoderados': apoderados,
    }
    return render(request, 'perfiles/mi_curso.html', context)