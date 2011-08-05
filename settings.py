
#
#
# 		if you do not agree to conditions set forth in README.txt, delete entire directory containing Bellum code and data NOW
#
#
#





























DEBUG = True
TEMPLATE_DEBUG = DEBUG

SMF_NAME = 'bellum_forum'
SMF_USER = 'root'
SMF_PASS = 'root'
SMF_HOST = 'localhost'

SMF_GROUP_UNALLIED = 5    # unallied SMF group
SMF_GROUP_ALLIED = 6    # allied SMF group
SMF_GROUP_LEADER = 7    # alliance leader SMF group

SMF_POST_GROUP = 4  # a post-dependent group

SMF_CAT_ALLIANCE = 2    # category ID for alliance forums


SMF_SECURITY_PROFILE = 1 # default security profile

DATABASE_ENGINE = 'mysql'      
DATABASE_NAME = 'bellum'       
DATABASE_USER = 'root'         
DATABASE_PASSWORD = 'root'     
DATABASE_HOST = 'localhost'    
DATABASE_PORT = ''             

TIME_ZONE = 'Europe/Warsaw'

LANGUAGE_CODE = 'pl'

SITE_ID = 1

USE_I18N = False

MEDIA_ROOT = 'D:/projects/webapps/bellum/media/'        # with trailing /

MEDIA_URL = 'http://bellum.localhost/media/'

SECRET_KEY = 'bydesireandambitiontheresahungestillunsatisfied'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'djangomako.middleware.MakoMiddleware',
    'bellum.orders.run.OrderMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

#INTERNAL_IPS = ('127.0.0.1', )

ROOT_URLCONF = 'bellum.urls'

#DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS':False}

TEMPLATE_DIRS = (
    'D:/projects/webapps/bellum/templates/',
#    'C:/Python25/Lib/site-packages/debug_toolbar/templates',
)

INSTALLED_APPS = (
    'django.contrib.sessions',
    'bellum.common',
    'bellum.alliance',
    'bellum.register',
    'bellum.uprofile',
    'bellum.mother',
    'bellum.province',
    'bellum.orders',
    'bellum.chat',
    'bellum.space',
    'bellum.landarmy',
    'bellum.stats',
    'bellum.portal',
#    'debug_toolbar',
)


MAKO_OUTPUT_ENCODING = 'utf-8'

CACHE_BACKEND = 'dummy:///'