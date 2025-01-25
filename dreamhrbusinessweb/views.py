from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Contact
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserRegistrationForm, UserLoginForm
from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request, 'iLanding/index.html')

def about(request):
    return render(request, 'about.html')

def pricing(request):
    return render(request, 'pricing.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        contact = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        # Send email
        email_subject = f'New Contact Form Submission: {subject}'
        email_message = f"""
        New contact form submission from {name}:

        Email: {email}
        Subject: {subject}
        Message:
        {message}
        """

        try:
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  # Send to admin email
                fail_silently=False,
            )
            
            # Send confirmation email to user
            user_subject = 'Thank you for contacting DreamHR-Ai'
            user_message = f"""
            Dear {name},

            Thank you for contacting us. We have received your message and will get back to you shortly.

            Your message details:
            Subject: {subject}
            Message: {message}

            Best regards,
            DreamHR-Ai Team
            """
            
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],  # Send to user's email
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again later.')
            print(f"Email error: {str(e)}")  # For debugging

        return redirect('index')  # Redirect back to home page

    return render(request, 'contact.html')

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Just save the user without logging in
            messages.success(request, 'Registration successful! Please login to continue.')
            return redirect('login')  # Redirect to login page
        return render(request, 'registration/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = UserLoginForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password.')
        return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        return render(request, 'registration/profile.html')

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            # Save to database
            contact = Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            # Send email to admin
            email_subject = f'New Contact Form Submission: {subject}'
            email_message = f"""
            New contact form submission from {name}:

            Email: {email}
            Subject: {subject}
            Message:
            {message}
            """

            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            
            # Send confirmation email to user
            user_subject = 'Thank you for contacting DreamHR-Ai'
            user_message = f"""
            Dear {name},

            Thank you for contacting us. We have received your message and will get back to you shortly.

            Your message details:
            Subject: {subject}
            Message: {message}

            Best regards,
            DreamHR-Ai Team
            """
            
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'success': False})

    return render(request, 'iLanding/index.html')
