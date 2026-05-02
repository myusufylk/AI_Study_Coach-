from django.contrib import admin
from django.urls import path
from core import views  # Views dosyasını toplu olarak içeri aktarıyoruz


urlpatterns = [

    # Yönetim Paneli
    path('admin/', admin.site.urls),

    # Ana Sayfa
    path('', views.home, name='home'),

    # Giriş Sayfası
    path('login/', views.login_view, name='login'),

    # Kayıt Sayfası
    path('register/', views.register_view, name='register'),

    # Çıkış
    path('logout/', views.logout_view, name='logout'),

    # Profil
    path('profile/', views.profile_view, name='profile'),

    # Ders seçim ekranı
    path('subjects/', views.subjects_view, name='subjects'),

    # Haftalık hedef
    path('weekly-goal/', views.weekly_goal_view, name='weekly_goal'),

    # AI ders programı oluştur
    path('generate-program/', views.generate_program, name='generate_program'),

    # AI koç sayfası
    path('ai-coach/', views.ai_coach_view, name='ai_coach'),

    # Ders İzleme sayfası
    path('lesson_watch/', views.lesson_watch, name='lesson_watch'),

    # API: YouTube videolarını getir
    path('api/get-videos/', views.api_get_videos, name='api_get_videos'),
]