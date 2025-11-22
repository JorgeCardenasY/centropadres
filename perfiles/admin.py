from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Perfil, Curso, Alumno
from centropadres.admin import my_admin_site

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'perfiles'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'alumno')
    list_filter = ('rol', 'alumno__curso')

# It's not ideal to unregister from the default site and register on another,
# but for this case it will work. A better solution would be to not register
# the User model on the default site in the first place.
admin.site.unregister(User)
my_admin_site.register(User, UserAdmin)
my_admin_site.register(Perfil, PerfilAdmin)
my_admin_site.register(Curso)
my_admin_site.register(Alumno)