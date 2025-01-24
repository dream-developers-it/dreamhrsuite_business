from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Contact

# Create your views here.

def home(request):
    return render(request, 'iLanding/index.html')

def about(request):
    return render(request, 'about.html')

def pricing(request):
    return render(request, 'pricing.html')

def register(request):
    return render(request, 'register.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        description = request.POST.get('description')
        
        # Save to database
        Contact.objects.create(
            name=name,
            email=email,
            description=description
        )
        
        # Send email
        subject = f'New Contact Form Submission from {name}'
        message = f'Name: {name}\nEmail: {email}\nMessage: {description}'
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again later.')
        
        # Redirect back to the same page with the contact form
        if request.path == '/contact/':
            return redirect('contact')
        return redirect('home')
    
    # If it's a GET request and the URL is /contact/, render the contact template
    if request.path == '/contact/':
        return render(request, 'contact.html')
    # Otherwise, the form is being accessed from the home page
    return render(request, 'iLanding/index.html')
