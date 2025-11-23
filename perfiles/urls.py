from django.urls import path
from . import views

# This file is intentionally left with an empty urlpatterns list.
# The old URL patterns were based on obsolete views.
urlpatterns = [
    path('mi-perfil/', views.mi_perfil, name='mi_perfil'),
    path('ajax/get-user-info/', views.get_user_info, name='get_user_info'),
]
