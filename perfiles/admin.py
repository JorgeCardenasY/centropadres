from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Perfil, Curso, Alumno

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'perfiles'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'alumno')
    list_filter = ('rol', 'alumno__curso')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Curso)
admin.site.register(Alumno)