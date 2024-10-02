from .base import *

DEBUG = bool(os.getenv("DJANGO_DEBUG", False))

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "<TODO>")

ALLOWED_HOSTS = ["ai-registry.lb.djnd.si"]
CSRF_TRUSTED_ORIGINS = ["https://ai-registry.lb.djnd.si"]
