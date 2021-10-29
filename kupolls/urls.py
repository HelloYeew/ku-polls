"""kupolls URL Configuration."""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from polls import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('polls/', include('polls.urls')),
    path('', RedirectView.as_view(url='polls/', permanent=True)),
    path('signup/', views.signup, name='signup'),
]
