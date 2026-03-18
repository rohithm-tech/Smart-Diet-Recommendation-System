"""
Django settings for diet_system project.
Production-ready for Render deployment.
"""

import os
from pathlib import Path
import dj_database_url

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ────────────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-x1b)r_b@+ur3td&@5jon1t$t&6iempmy0f1+ul=+7@+a@^!si8')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
RENDER = os.environ.get('RENDER', 'False').lower() == 'true'

ALLOWED_HOSTS = []
if RENDER:
    ALLOWED_HOSTS.append(os.environ.get('RENDER_EXTERNAL_HOSTNAME', ''))
if not RENDER:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])

# ── Apps ────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'recommender',
]

# ── Middleware ──────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',       # Serve static in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'diet_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'diet_system.wsgi.application'

# ── Database ───────────────────────────────────────────────────
# Uses SQLite locally, PostgreSQL on Render (via DATABASE_URL env var)
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
    )
}

# ── Password Validation ────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internationalization ───────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ── Static Files ───────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ── Auth ───────────────────────────────────────────────────────
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Production Security ────────────────────────────────────────
if RENDER:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = [f'https://{os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")}']
