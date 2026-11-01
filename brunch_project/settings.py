"""Setarile proiectului Brunch & Bloom."""

from pathlib import Path

# Folderul in care se afla proiectul.
BASE_DIR = Path(__file__).resolve().parent.parent


# Setari pentru rularea locala a proiectului.

# Cheia secreta nu se publica pentru un site folosit online.
SECRET_KEY = 'django-insecure-buq_b)qojjcai^nvy0i1pf2gnd0#*tp#d@t0!(_mc*dxoz(^er'

# Afisam detaliile erorilor cat timp lucram local.
DEBUG = True

ALLOWED_HOSTS = []


# Aplicatiile si middleware-urile folosite.

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'brunch',
]

MIDDLEWARE = [
    'brunch.middleware.IPClientMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'brunch_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'brunch.context_processors.date_firma',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'brunch_project.wsgi.application'


# Baza de date.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Reguli pentru parolele utilizatorilor.

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Limba si fusul orar.

LANGUAGE_CODE = 'ro'

TIME_ZONE = 'Europe/Bucharest'

USE_I18N = True

USE_TZ = True


# Adresa fisierelor statice: CSS si imagini.

STATIC_URL = 'static/'

# Tipul implicit al ID-urilor din baza de date.

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Date de exemplu pentru firma din proiect.
FIRMA = {
    "nume": "Brunch & Bloom",
    "an_infiintare": 2026,
    "telefon": "0747539299",
    "adresa": "București - Strada Gurmanzilor nr.53",
    "email": "contact@brunch-bloom.com",
    "specific": "Brunch și late breakfast",
}


# Imaginile incarcate din admin se pastreaza separat de fisierele statice.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
