from django.contrib import admin
from django.urls import path
from core import views # Views dosyasını toplu olarak içeri aktarıyoruz

urlpatterns = [
    # Yönetim Paneli
    path('admin/', admin.site.urls),

    # Ana Sayfa (localhost:8000)
    path('', views.home, name='home'),

    # Giriş Sayfası (localhost:8000/login/)
    # Buradaki name='login' değeri, redirect('login') komutunun hedefidir.
    path('login/', views.login_view, name='login'),

    # Kayıt Sayfası (localhost:8000/register/)
    path('register/', views.register_view, name='register'),

    # Çıkış İşlemi
    path('logout/', views.logout_view, name='logout'),
]