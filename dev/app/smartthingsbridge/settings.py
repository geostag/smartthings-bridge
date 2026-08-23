from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-development-key")
DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"

ALLOWED_HOSTS = [
    h.strip() for h in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "localhost,127.0.0.1"
    ).split(",") if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
] if os.getenv("PUBLIC_BASE_URL") else []

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "bridgeapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "smartthingsbridge.urls"
TEMPLATES = []
WSGI_APPLICATION = "smartthingsbridge.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/data/bridge.sqlite3",
    }
}

LANGUAGE_CODE = "de-de"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SMARTTHINGS_API_BASE_URL = os.getenv(
    "SMARTTHINGS_API_BASE_URL",
    "https://api.smartthings.com/v1",
)
SMARTTHINGS_CLIENT_ID = os.getenv("SMARTTHINGS_CLIENT_ID", "")
SMARTTHINGS_CLIENT_SECRET = os.getenv("SMARTTHINGS_CLIENT_SECRET", "")
SMARTTHINGS_REDIRECT_URI = os.getenv(
    "SMARTTHINGS_REDIRECT_URI",
    "http://localhost:8080/oauth/callback",
)

PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "http://localhost:8080")

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_TOPIC_PREFIX = os.getenv("MQTT_TOPIC_PREFIX", "smartthings")
MQTT_TLS = os.getenv("MQTT_TLS", "0") == "1"

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
