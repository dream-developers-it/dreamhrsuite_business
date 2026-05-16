import os

import requests
from django.conf import settings


def verify_turnstile(request):
    """
    Verify Cloudflare Turnstile token from POST data.
    Skips verification when TURNSTILE_SECRET_KEY is not configured.
    Returns (ok: bool, error_message: str | None).
    """
    secret = getattr(settings, 'TURNSTILE_SECRET_KEY', '') or os.getenv('TURNSTILE_SECRET_KEY', '')
    if not secret:
        return True, None

    token = request.POST.get('cf-turnstile-response')
    if not token:
        return False, 'Please complete the security check.'

    try:
        response = requests.post(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify',
            data={
                'secret': secret,
                'response': token,
                'remoteip': request.META.get('REMOTE_ADDR'),
            },
            timeout=10,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException:
        return False, 'Security check could not be verified. Please try again.'

    if result.get('success'):
        return True, None

    return False, 'Security check failed. Please try again.'
