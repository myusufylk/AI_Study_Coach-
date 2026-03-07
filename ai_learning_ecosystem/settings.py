from pathlib import Path
import os
import mimetypes # CSS tasarımı için kritik

# Proje yollarını otomatik algılar
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-h#i^^gw%om-5m13h%t7ru(f=+wt**l0v#^kj&tn6tjg8#ai^g^'

DEBUG = True # Geliştirme aşamasında hataları görmek için True 

ALLOWED_HOSTS = ['*'] # Arkadaşlarının erişimi için esnetildi

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core', # Senin uygulama klasörün 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ai_learning_ecosystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Şablon yolunu dinamik yaptık 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ai_learning_ecosystem.wsgi.application'

# DATABASE AYARI (EKİP İÇİN DÜZELTİLDİ)
# Arkadaşların bağlandığında HOST kısmını kendi bilgisayar adlarıyla değiştirmeli 
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'AI_Koc_DB', 
        'HOST': 'YUSUF', # Senin bilgisayarında 'YUSUF' kalabilir 
        'USER': '',           
        'PASSWORD': '',      
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'unicode_results': True,
            'trusted_connection': 'yes', # Windows Authentication için eklendi
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Dil ve Zaman Ayarları
LANGUAGE_CODE = 'tr-tr' # Yönetim panelini Türkçe yaptık
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

# STATİK DOSYA AYARLARI (TASARIMIN GELMESİ İÇİN KRİTİK)
mimetypes.add_type("text/css", ".css", True) # Beyaz ekran sorununu çözer
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] # Tasarımı bulması için yolu sabitledik 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'