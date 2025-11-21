from django.urls import path
from .views import mi_curso, PerfilCreateView, PerfilUpdateView, PerfilDeleteView, PerfilesExplanationView

urlpatterns = [
    path('', mi_curso, name='mi-curso'),
    path('crear/', PerfilCreateView.as_view(), name='perfil-create'),
    path('<int:pk>/editar/', PerfilUpdateView.as_view(), name='perfil-update'),
    path('<int:pk>/eliminar/', PerfilDeleteView.as_view(), name='perfil-delete'),
    path('explicacion/', PerfilesExplanationView.as_view(), name='perfiles-explanation'),
]
