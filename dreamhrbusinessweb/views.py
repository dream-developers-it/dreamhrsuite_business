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
import requests
import os
from pathlib import Path
import dotenv

# Create your views here.

def home(request):
    return render(request, 'iLanding/index.html')

# def about(request):
#     return render(request, 'about.html')

# def pricing(request):
#     return render(request, 'pricing.html')

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

            # Send Slack notification
            send_slack_notification(name, email, subject, message)

            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again later.')
            print(f"Email error: {str(e)}")  # For debugging

        return redirect('index')  # Redirect back to home page

    return render(request, 'contact.html')

def send_slack_notification(name, email, subject, message):
    webhook_url = os.getenv('SLACK_CONTACT_WEBHOOK')
    print(f"Contact Webhook URL from env: {webhook_url}")
    
    # Reload environment variables to ensure we have the latest
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / '.env'
    print(f"Reloading .env from: {env_path}")
    load_dotenv(env_path)
    
    # Get the URL again after reload
    webhook_url = os.getenv('SLACK_CONTACT_WEBHOOK')
    print(f"Contact Webhook URL after reload: {webhook_url}")
    
    if not webhook_url:
        print("Error: SLACK_CONTACT_WEBHOOK environment variable is not set")
        return False
    
    slack_message = {
        "text": "New Contact Form Submission",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*New Contact Form Submission*"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Name:*\n{name}"},
                    {"type": "mrkdwn", "text": f"*Email:*\n{email}"},
                    {"type": "mrkdwn", "text": f"*Subject:*\n{subject}"},
                    {"type": "mrkdwn", "text": f"*Message:*\n{message}"}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(webhook_url, json=slack_message)
        if response.status_code == 404:
            print(f"Error: Webhook URL not found (404). Please check if the URL is correct.")
        elif response.status_code != 200:
            print(f"Error: Slack API returned status code {response.status_code}")
            print(f"Response text: {response.text}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending Slack notification: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Error details: {e.response.text}")
        return False

def send_registration_slack_notification(user):
    webhook_url = os.getenv('SLACK_REGISTRATION_WEBHOOK')
    
    if not webhook_url:
        print("Error: SLACK_REGISTRATION_WEBHOOK environment variable is not set")
        return False
    
    # Get full name or use email if name not provided
    full_name = f"{user.first_name} {user.last_name}".strip()
    display_name = full_name if full_name else user.email
    
    slack_message = {
        "text": "New User Registration",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "* New User Registration*"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Name:*\n{display_name}"},
                    {"type": "mrkdwn", "text": f"*Email:*\n{user.email}"}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(webhook_url, json=slack_message)
        if response.status_code == 404:
            print(f"Error: Webhook URL not found (404). Please check if the URL is correct.")
        elif response.status_code != 200:
            print(f"Error: Slack API returned status code {response.status_code}")
            print(f"Response text: {response.text}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending registration Slack notification: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Error details: {e.response.text}")
        return False

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('profile')
        
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Send Slack notification for new registration
            send_registration_slack_notification(user)
            
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
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

            # Send Slack notification
            send_slack_notification(name, email, subject, message)

            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'success': False})

    return render(request, 'iLanding/index.html')
