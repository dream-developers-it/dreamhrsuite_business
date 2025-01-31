from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from django.contrib.sitemaps.views import sitemap
from .sitemap import StaticViewSitemap, DynamicViewSitemap
from django.http import FileResponse
import os

sitemaps = {
    'static': StaticViewSitemap,
    'dynamic': DynamicViewSitemap,
}

def serve_robots_txt(request):
    robots_file = os.path.join(settings.BASE_DIR, 'robots.txt')
    return FileResponse(open(robots_file, 'rb'), content_type='text/plain')

urlpatterns = [
    path('dreamhr-business/', admin.site.urls),
    path('', include('dreamhrbusinessweb.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('dreamhrbusinessweb.urls')),
    path('robots.txt', serve_robots_txt, name='robots_txt'),
    
    # Serve static files in production
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Add this only for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
