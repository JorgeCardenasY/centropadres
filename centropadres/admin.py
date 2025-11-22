from django.contrib.admin import AdminSite
from .forms import MyCustomAuthenticationForm

class MyAdminSite(AdminSite):
    login_form = MyCustomAuthenticationForm
    login_template = 'admin/login.html'
    site_header = "SchoolPay Admin"

my_admin_site = MyAdminSite(name='myadmin')
