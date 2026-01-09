# ai_finance_tracker/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# =================================================
# BASE
# =================================================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# =================================================
# SECURITY
# =================================================
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("❌ SECRET_KEY not set")

DEBUG = os.getenv("DEBUG", "False").lower() in {"1", "true", "yes"}

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    ".onrender.com,localhost,127.0.0.1"
).split(",")

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# =================================================
# APPLICATIONS
# =================================================
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

   

    # Project apps
    "accounts.apps.AccountsConfig",
    "transactions",
    "insights",
]



# =================================================
# MIDDLEWARE
# =================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",



    "django.contrib.messages.middleware.MessageMiddleware",

    # optional but safe
    "accounts.middleware.ActiveUserMiddleware",
]

# =================================================
# URLS / TEMPLATES
# =================================================
ROOT_URLCONF = "ai_finance_tracker.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ai_finance_tracker.wsgi.application"

# =================================================
# DATABASE
# =================================================
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL not set")

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=True,
    )
}

# =================================================
# INTERNATIONALIZATION
# =================================================
LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# =================================================
# STATIC FILES (RENDER SAFE)
# =================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

# =================================================
# AUTH / ALLAUTH (CRITICAL FIXES)
# =================================================
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "transactions:dashboard"
LOGOUT_REDIRECT_URL = "login"



# =================================================
# DEFAULT PK
# =================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
