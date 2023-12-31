"""
URL configuration for wetcave project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
        path("dashboard/", include("dashboard.urls")),
        path("", RedirectView.as_view(pattern_name='dashboard:index')),
        path("settings/", include("settings.urls")),
        path("accounts/", include("django.contrib.auth.urls")),
        path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.png'))),
        path("__reload__/", include("django_browser_reload.urls")),
        path('django_plotly_dash/', include('django_plotly_dash.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.ADMIN_ENABLED is True:
    urlpatterns += [path('admin/', admin.site.urls),]
