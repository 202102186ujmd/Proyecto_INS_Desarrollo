# cls
from pathlib import Path
import os  # Asegúrate de que esta línea esté presente

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de desarrollo
# Ver https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wantifec@(&h-_*s_3a^1=4m@2afggpb_)^3r=_&)syf()8#yl'

# SECURITY WARNING: no ejecutes con el modo de depuración activado en producción!
DEBUG = True

# Permite que cualquier host acceda a la aplicación
ALLOWED_HOSTS = ['*']

# Lista de aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #aplicaiones personalizadas
    'acceso_evento',
    'administracion',
    'analisis_datos',
    'api_calendario',
    'archivos',
    'autenticacion',
    'calendario',
    'contenido',
    'evaluaciones',
    'gestion_eventos',
    'notificaciones',
    'participantes',
    'reportes',
    'soporte',
]

# Middleware de seguridad
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Gestion_Eventos_INS.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'administracion.context_processors.user_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'Gestion_Eventos_INS.wsgi.application'


# Configuración de la base de datos
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Motor de base de datos
        'NAME': 'proyecto_django',  # Nombre de la base de datos
        'USER': 'proyectodjango',          # Usuario de la base de datos
        'PASSWORD': 'proyectodjango',       # Contraseña del usuario
        'HOST': 'localhost',         # Host de la base de datos
        'PORT': '3306',              # Puerto de la base de datos
    }   
}


# Validación de contraseñas
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internacionalización
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# Idioma de la aplicación
LANGUAGE_CODE = 'es-ES'

# Zona horaria de El Salvador
TIME_ZONE = 'America/El_Salvador'

# Usar internacionalización
USE_I18N = True
USE_TZ = True


# Archivos estáticos (CSS, JavaScript, Imágenes)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Tipo de campo de clave primaria predeterminado
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de autenticación
AUTH_USER_MODEL = 'autenticacion.Usuario'

# Configuración de redireccionamiento de inicio de sesión y cierre de sesión
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login' 
 

#Configuración de correo para recuperación de contraseña
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'proyectoeventosins@gmail.com'
EMAIL_HOST_PASSWORD = 'ticp kpfz ywzg lofz'
DEFAULT_FROM_EMAIL = 'proyectoeventosins@gmail.com'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')