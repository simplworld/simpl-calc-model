import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "qyitw1&uc^db0)ds@yeaw+tc7baqak@ufa#!9m4919s86zqjv^"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["model.backend", "localhost"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Simpl model service apps
    "modelservice",
    "game",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "simpl_calc_model.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "simpl_calc_model.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = "/static/"

# set Simpl users cache
CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
    "users": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "users",
    },
}

# define Simpl model service properties

# Where simpl-games-api should send webhooks to update the model service of
# changes to the data
CALLBACK_URL = os.environ.get("CALLBACK_URL", "http://{hostname}:{port}/callback")

# The URL for the simpl-games-api service
SIMPL_GAMES_URL = os.environ.get("SIMPL_GAMES_URL", "http://localhost:8100/apis")

# The user/password that is setup for the model service to authenticate to the
# simpl-games-api.  NOTE: This user must have `is_staff=True` on the Django user.
SIMPL_GAMES_AUTH = ("simpl@simpl.world", "simpl")

# Shared secret between the crossbar process and "guest" model service process.
# This just needs to be something long and random it's only used between these
# to processes in this container.
MODEL_TICKET = "msZhFboHtsW1zLn3Bj4yp6jQ"

EXTERNAL_AUTH_SHARED_SECRET = "simpl-calc-NmTnZCgcTpPgtsbw"

# The root topic for this simulation/game
ROOT_TOPIC = "world.simpl.sims.simpl-calc"

GAME_SLUG = 'simpl-calc'
