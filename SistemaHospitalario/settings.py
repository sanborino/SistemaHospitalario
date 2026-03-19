
from pathlib import Path
import environ, dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = "acceso.Usuario"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# Proteger variables de entorno
env = environ.Env()
environ.Env.read_env()

SECRET_KEY = 'SECRET_KEY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DEBUG'

ALLOWED_HOSTS = ['.onrender.com', 'localhost']

"""CSRF_TRUSTED_ORIGINS = [
    'http://192.168.1.186:8000',
]"""


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'SistemaHospitalario',
    'acceso.apps.AccesoConfig',
    'auditoria.apps.AuditoriaConfig',
    'cita',
    'facturacion',
    'farmacia',
    'historial',
    'hospital',
    'infraestructura',
    'inventario',
    'laboratorio',
    'paciente',
    'personal',
    'turno',
    'urgencia'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SistemaHospitalario.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'SistemaHospitalario' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "SistemaHospitalario.context_processors.roles_usuario",
            ],
        },
    },
]

WSGI_APPLICATION = 'SistemaHospitalario.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sistemahospitalario',
        'USER': 'root',
        'PASSWORD': 'toor',
        'HOST': 'localhost',
        'PORT': 3306
    }
}

"""DATABASES = {
    'default': dj_database_url.config( 
        conn_max_age=600,
        conn_health_checks=True,
    ),

        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'sistemahospitalario',
        #'USER': 'sistemahospitalario_user',
        #'PASSWORD': 'PASSWORD',
        #'HOST': 'HOST',
        #'PORT': '5432',
    }
"""


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "SistemaHospitalario" / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# Media

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'EMAIL_HOST_USER'
EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD'


LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = 'hospital/'




