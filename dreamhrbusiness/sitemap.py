from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        # Add all your static pages here
        return [
            'index',
            'login',
            'about',
            'features',
            'services',
            'pricing',
            'contact'
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        # Return the last modification date
        return timezone.now()

class DynamicViewSitemap(Sitemap):
    priority = 0.6
    changefreq = 'daily'
    protocol = 'https'

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
