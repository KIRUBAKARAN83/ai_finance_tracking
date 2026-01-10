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

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com",
    ".railway.app",
]

# Trusted origins for CSRF (keep wildcard for onrender)
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
    "accounts",
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

    # Active user tracker (defensive implementation recommended)
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
        conn_max_age=int(os.getenv("DB_CONN_MAX_AGE", 600)),
        ssl_require=os.getenv("DB_SSL_REQUIRE", "True").lower() in {"1", "true", "yes"},
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

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# =================================================
# AUTH / LOGIN CONFIG
# =================================================
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "transactions:dashboard"
LOGOUT_REDIRECT_URL = "login"

# =================================================
# DEFAULT PK
# =================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =================================================
# LOGGING (prints errors to stdout so Render shows tracebacks)
# =================================================
import logging.config

LOG_LEVEL = "DEBUG" if DEBUG else "ERROR"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(levelname)s %(asctime)s %(name)s %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        # reduce noise from some libraries
        "django.db.backends": {"level": "ERROR", "handlers": ["console"], "propagate": False},
    },
}
