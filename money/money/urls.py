# finance/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('monzo_app.urls')),  # serve monzo_app at the site root
]
