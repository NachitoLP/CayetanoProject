from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'CAYETANO_DB',
        'USER': secret["DB_USER"],
        'PASSWORD': secret['DB_PASSWORD'],
        'HOST': 'FX-NB-001\MSSQLSERVER02',
        'PORT': '',
        'OPTIONS': {'driver': 'ODBC Driver 17 for SQL Server', 'extra_params': 'TrustServerCertificate=yes;'}
    }
}


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


LANGUAGE_CODE = 'es-AR'

USE_TZ = True
TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'public')
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#COOKIES y SESSION

SESSION_EXPIRE_AT_BROWSER_CLOSE = True #Se cierra la sesión al cerrar el navegador

SESSION_COOKIE_AGE = 3600 #1 Hora
SESSION_SAVE_EVERY_REQUEST = True #Se reestablece con cada acción