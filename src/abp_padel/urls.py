"""abp_padel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from users.views import signup_view, profile_view, LoginView, LogoutView, inscripcion_view, desinscripcion_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('signup/', signup_view, name='users-signup'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='users-login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='users-logout'),
    path('profile/', profile_view, name='users-profile'),
    path('inscripcion/', inscripcion_view, name='users-inscripcion'),
    path('desinscripcion/', desinscripcion_view, name='users-desinscripcion'),
    path('pista/', include('pistas.urls')),
    path('reserva/', include('reservas.urls')),
    path('campeonato/', include('campeonatos.urls')),
    path('partidos-promocionados/', include('promociones_partidos.urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.index_title = "iPadl Admin"
admin.site.site_header = "iPadl Admin"
