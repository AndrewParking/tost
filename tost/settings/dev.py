import os
from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')