import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# -------------------------------------------------
# BASE
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env when running locally; in Render, use Dashboard env vars
load_dotenv(BASE_DIR / ".env")

# -------------------------------------------------
# SECURITY
# -------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("❌ SECRET_KEY is not set")

# In production on Render, keep DEBUG False. Allow override via env if needed.
DEBUG = os.getenv("DEBUG", "False").lower() in {"1", "true", "yes"}

# Hosts: include your custom domain if you have one
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", ".onrender.com,localhost,127.0.0.1").split(",")

# CSRF: include Render domain and any custom domains over HTTPS
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]
_custom_csrf = os.getenv("CSRF_TRUSTED_ORIGINS")
if _custom_csrf:
    CSRF_TRUSTED_ORIGINS += [x.strip() for x in _custom_csrf.split(",") if x.strip()]

# Secure cookies and HTTPS headers
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True  # Render provides HTTPS by default

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
REFERRER_POLICY = "same-origin"

# -------------------------------------------------
# APPLICATIONS
# -------------------------------------------------
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local apps
    "accounts",
    "transactions",
    "insights",
]

# -------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    "accounts.middleware.ActiveUserMiddleware",
]

# -------------------------------------------------
# URLS / TEMPLATES
# -------------------------------------------------
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

# -------------------------------------------------
# DATABASE
# -------------------------------------------------
# Render sets DATABASE_URL for Postgres automatically.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL not set")

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,    # keep-alive for performance
        ssl_require=True,    # enforce SSL on Render
    )
}

# -------------------------------------------------
# INTERNATIONALIZATION
# -------------------------------------------------
LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------
# STATIC FILES
# -------------------------------------------------
# Use WhiteNoise for static files in production.
STATIC_URL = "/static/"

# Local static assets you want to include (optional; keep if you have a 'static' dir)
STATICFILES_DIRS = [BASE_DIR / "static"]

# Collected static files target (Render's disk is ephemeral but fine for static)
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Cache headers via WhiteNoise
WHITENOISE_MAX_AGE = 31536000  # 1 year for immutable files

# -------------------------------------------------
# MEDIA (optional, avoid local disk on Render)
# -------------------------------------------------
# If you need user-uploaded files, use a cloud storage (S3, etc.)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"  # Not recommended for persistent storage on Render

# -------------------------------------------------
# AUTH
# -------------------------------------------------
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "transactions:dashboard"
LOGOUT_REDIRECT_URL = "login"

# -------------------------------------------------
# LOGGING (production-friendly defaults)
# -------------------------------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

# -------------------------------------------------
# DEFAULT PK
# -------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
