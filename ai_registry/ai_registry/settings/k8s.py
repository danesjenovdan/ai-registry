from .base import *

DEBUG = bool(os.getenv("DJANGO_DEBUG", False))

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "<TODO>")

ALLOWED_HOSTS = [
    "registerui.djnd.si",
    "registerui.danesjenovdan.si",
]
CSRF_TRUSTED_ORIGINS = [
    "https://registerui.djnd.si",
    "https://registerui.danesjenovdan.si",
]

STATIC_ROOT = os.getenv("DJANGO_STATIC_ROOT", BASE_DIR / "staticfiles")
STATIC_URL = os.getenv("DJANGO_STATIC_URL_BASE", "static/")

if os.getenv("DJANGO_ENABLE_S3", False):
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    }
    AWS_ACCESS_KEY_ID = os.getenv("DJANGO_AWS_ACCESS_KEY_ID", "<TODO>")
    AWS_SECRET_ACCESS_KEY = os.getenv("DJANGO_AWS_SECRET_ACCESS_KEY", "<TODO>")
    AWS_STORAGE_BUCKET_NAME = os.getenv("DJANGO_AWS_STORAGE_BUCKET_NAME", "djnd")
    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False
    AWS_LOCATION = os.getenv("DJANGO_AWS_LOCATION", "ai-registry")
    AWS_S3_REGION_NAME = os.getenv("DJANGO_AWS_REGION_NAME", "fr-par")
    AWS_S3_ENDPOINT_URL = os.getenv(
        "DJANGO_AWS_S3_ENDPOINT_URL", "https://s3.fr-par.scw.cloud"
    )
    AWS_S3_SIGNATURE_VERSION = os.getenv("DJANGO_AWS_S3_SIGNATURE_VERSION", "s3v4")
    AWS_S3_FILE_OVERWRITE = False

if sentry_url := os.getenv("DJANGO_SENTRY_URL", False):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=sentry_url,
        integrations=[
            DjangoIntegration(),
        ],
        environment=os.getenv("SENTRY_ENV", "production"),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", 0.001)),
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

if os.getenv("DJANGO_ENABLE_MEMCACHED", False):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
            "LOCATION": os.getenv("DJANGO_MEMCACHED_LOCATION", None),
            "TIMEOUT": None,
            "KEY_PREFIX": os.getenv("DJANGO_MEMCACHED_KEY_PREFIX", "ai_registry_"),
            "OPTIONS": {
                "binary": True,
                "username": os.getenv("DJANGO_MEMCACHED_USERNAME", ""),
                "password": os.getenv("DJANGO_MEMCACHED_PASSWORD", ""),
                "behaviors": {
                    "tcp_nodelay": True,
                },
            },
        }
    }
