from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .forms import MyCustomAuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session # Import Session
from perfiles.models import Apoderado # Import Apoderado
from django.utils import timezone # Import timezone

class MyAdminSite(AdminSite):
    login_form = MyCustomAuthenticationForm
    login_template = 'admin/login.html'
    site_header = "SchoolPay Admin"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('permissions-dashboard/', self.admin_view(self.permissions_dashboard), name='permissions_dashboard'),
            path('manage-apoderado-sessions/', self.admin_view(self.manage_apoderado_sessions), name='manage_apoderado_sessions'), # New URL
        ]
        return my_urls + urls

    def login(self, request, extra_context=None):
        # Call the parent AdminSite's login method
        response = super().login(request, extra_context)

        # If the user is authenticated and is not a staff member, redirect them
        if request.user.is_authenticated and not request.user.is_staff:
            return HttpResponseRedirect('/perfiles/mi-perfil/')
        
        return response

    def permissions_dashboard(self, request):
        # Only superusers can access this page
        if not request.user.is_superuser:
            return render(request, 'admin/denied.html', {'message': 'No tiene permisos para acceder a esta página.'})

        users = User.objects.filter(is_superuser=False)
        context = {
            'title': 'Panel de Permisos',
            'users': users,
            **self.each_context(request),
        }
        return render(request, 'admin/permissions_dashboard.html', context)

    def manage_apoderado_sessions(self, request):
        # Only superusers can access this page
        if not request.user.is_superuser:
            return render(request, 'admin/denied.html', {'message': 'No tiene permisos para acceder a esta página.'})

        if request.method == 'POST':
            session_keys_to_delete = request.POST.getlist('session_keys')
            for session_key in session_keys_to_delete:
                try:
                    Session.objects.get(session_key=session_key).delete()
                except Session.DoesNotExist:
                    pass # Session already expired or deleted
            self.message_user(request, f"{len(session_keys_to_delete)} sesiones seleccionadas han sido cerradas.", level='success')
            return redirect('myadmin:manage_apoderado_sessions')

        active_sessions_data = []
        for session in Session.objects.filter(expire_date__gte=timezone.now()):
            session_data = session.get_decoded()
            user_id = session_data.get('_auth_user_id')
            if user_id:
                try:
                    user = User.objects.get(pk=user_id)
                    # Check if the user is an Apoderado and not staff/superuser
                    if hasattr(user, 'apoderado') and not user.is_staff and not user.is_superuser:
                        active_sessions_data.append({
                            'session_key': session.session_key,
                            'username': user.username,
                            'apoderado_name': f"{user.apoderado.nombres} {user.apoderado.apellidos}",
                            'last_activity': session.expire_date # This is actually session expiry
                        })
                except User.DoesNotExist:
                    pass # User associated with session no longer exists

        context = {
            'title': 'Gestionar Sesiones de Apoderados',
            'active_sessions': active_sessions_data,
            **self.each_context(request),
        }
        return render(request, 'admin/manage_apoderado_sessions.html', context)

my_admin_site = MyAdminSite(name='myadmin')

my_admin_site.register(User, UserAdmin)
my_admin_site.register(Group, GroupAdmin)