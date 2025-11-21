from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Enviar email (opcional - requiere configuración SMTP)
        try:
            subject = f'Mensaje de contacto de {name}'
            email_message = f"""
            Nombre: {name}
            Email: {email}
            
            Mensaje:
            {message}
            """
            
            # Descomentar cuando tengas SMTP configurado
            # send_mail(
            #     subject,
            #     email_message,
            #     settings.DEFAULT_FROM_EMAIL,
            #     [settings.CONTACT_EMAIL],
            #     fail_silently=False,
            # )
            
            messages.success(request, '¡Gracias por tu mensaje! Te contactaremos pronto.')
        except Exception as e:
            messages.error(request, 'Hubo un error al enviar tu mensaje. Por favor, intenta nuevamente.')
        
        return redirect('home')
    
    return redirect('home')
