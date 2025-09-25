# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Cesta pro Django administraci
    path('admin/', admin.site.urls),
    # Cesta pro přehled úkolů
    path('tasks/', include('tasks.urls')),
]