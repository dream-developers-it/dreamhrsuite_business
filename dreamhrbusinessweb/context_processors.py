from django.conf import settings


def turnstile(request):
    site_key = ''
    if settings.TURNSTILE_SITE_KEY and settings.TURNSTILE_SECRET_KEY:
        site_key = settings.TURNSTILE_SITE_KEY
    return {'turnstile_site_key': site_key}
