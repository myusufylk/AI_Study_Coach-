from django.contrib import admin
from django.urls import path
from core.views import home, login_view, register_view # Hepsini tek satırda topladık

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Ana sayfa bağlantısı (Tarayıcıya sadece 127.0.0.1:8000 yazınca açılır)
    path('', home, name='home'), 
    
    # Giriş ve Kayıt sayfaları
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
]