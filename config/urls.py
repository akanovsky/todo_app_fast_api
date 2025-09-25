# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView # Nový import


urlpatterns = [
    # Cesta pro Django administraci
    path('admin/', admin.site.urls),
    # Cesta pro přehled úkolů
    path('tasks/', include('tasks.urls')),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Přesměrování po odhlášení
]