from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-p#rcl1k19s6(1wqijda3884s@k%a=8o2oy992l+o4l*dc$4%d-"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]


# debug toolbar settings
def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    "RESULTS_CACHE_SIZE": 500,
}
