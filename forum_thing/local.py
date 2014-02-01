
from unipath import Path
from django.core.urlresolvers import reverse_lazy

SECRET_KEY = 'p$ix2#(50ohb6d)d6mxqoz-@s_maw4or^mcuq#2=xjwlby3n9a'

PROJECT_DIR = Path(__file__).ancestor(2)

TEMPLATE_DIRS = (
    PROJECT_DIR.child("templates"),
)

STATICFILES_DIRS = (
    PROJECT_DIR.child("static"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.media",
    "django.core.context_processors.static",
)

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_URL = reverse_lazy('logout')

# Application definition
DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

THIRD_PARTY_APPS = (
    'braces',
    'registration',
    'django_extensions',
    'south',
    'taggit',
    'crispy_forms',
    'debug_toolbar',
    'widget_tweaks',
)

LOCAL_APPS = (
    'post',
)

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

ROOT_URLCONF = 'forum_thing.urls'

WSGI_APPLICATION = 'forum_thing.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_DIR.child('db.sqlite3'),
    }
}

SITE_URL = "127.0.0.0:8000"
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
#EMAIL_HOST = 'localhost'
#EMAIL_PORT = '1025'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

def custom_show_toolbar(request):
    return True
