from .base import *

DEBUG = bool(os.getenv("DJANGO_DEBUG", False))

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "<TODO>")

ALLOWED_HOSTS = ["ai-register.lb.djnd.si"]
CSRF_TRUSTED_ORIGINS = ["https://ai-register.lb.djnd.si"]
