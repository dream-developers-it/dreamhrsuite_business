from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    protocol = 'https' if not settings.DEBUG else 'http'

    def items(self):
        # Only include URLs that actually exist in your urls.py
        return [
            'index',
            # 'about',
            # 'pricing',
            'contact',
            'login',
            'register',
            # 'profile'
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()

class DynamicViewSitemap(Sitemap):
    priority = 0.6
    changefreq = 'daily'
    protocol = 'https' if not settings.DEBUG else 'http'

    def items(self):
        # Add your dynamic models here if you have any
        # Example: return YourModel.objects.all()
        return []

    def location(self, item):
        # Example: return item.get_absolute_url()
        return item.get_absolute_url()

    def lastmod(self, item):
        # Example: return item.updated_at
        return item.updated_at
