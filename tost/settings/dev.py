import os
import sys
from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'popow.andrej2009'
EMAIL_HOST_PASSWORD = 'homm1994'
DEFAULT_FROM_EMAIL = 'popow.andrej2009@gmail.com'
DEFAULT_TO_EMAIL = 'to email'


if 'test' in sys.argv:
	DATABASES['default'] = {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': 'test',
		'USER': 'test',
		'PASSWORD': 'test',
	}
