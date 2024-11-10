from .base import *

load_dotenv()

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'disable',
        },
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
DATE_INPUT_FORMATS = ['%d/%m/%Y', '%Y-%m-%d']

USE_I18N = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'public')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#COOKIES y SESSION

SESSION_EXPIRE_AT_BROWSER_CLOSE = True #Se cierra la sesión al cerrar el navegador

SESSION_COOKIE_AGE = 3600 #1 Hora
SESSION_SAVE_EVERY_REQUEST = True #Se reestablece con cada acción