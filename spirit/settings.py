#-*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE
# YOU MAY OVERWRITE THE DEFAULT VALUES IN YOUR settings.py FILE

import os

ST_COMMENTS_PER_PAGE = 20
ST_COMMENTS_PAGE_VAR = 'page'

ST_TOPIC_PRIVATE_CATEGORY_PK = 1
ST_UNCATEGORIZED_CATEGORY_PK = 2

ST_RATELIMIT_ENABLE = True
ST_RATELIMIT_CACHE_PREFIX = 'srl'
ST_RATELIMIT_CACHE = 'default'

ST_NOTIFICATIONS_PER_PAGE = 20

ST_MENTIONS_PER_COMMENT = 30

ST_YT_PAGINATOR_PAGE_RANGE = 3

ST_SEARCH_QUERY_MIN_LEN = 3

ST_USER_LAST_SEEN_THRESHOLD_MINUTES = 1

# check out http://pythonhosted.org/Markdown/extensions/index.html
ST_MARKDOWN_EXT = (
    'nl2br',
    'spirit.utils.markdown.mention',
    'spirit.utils.markdown.emoji',
    'spirit.utils.markdown.image',
    'spirit.utils.markdown.video',
    'spirit.utils.markdown.audio',
    'spirit.utils.markdown.youtube',
    'spirit.utils.markdown.vimeo',
    'spirit.utils.markdown.mathjax',
)


#
# Django settings defined below...
#

# django-djconfig
DJC_BACKEND = 'djconfig'

# django-haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

# python manage.py createcachetable spirit_cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'spirit_cache',
    },
    # django-djconfig
    'djconfig': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}

LOCALE_PATHS = [os.path.join(os.path.dirname(__file__), 'locale'), ]

AUTH_USER_MODEL = 'spirit.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'spirit.backends.user.EmailAuthBackend',
)

LOGIN_URL = 'spirit:user-login'
LOGIN_REDIRECT_URL = 'spirit:profile-update'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djconfig.middleware.DjConfigLocMemMiddleware',  # django-djconfig
    #'spirit.middleware.XForwardedForMiddleware',
    'spirit.middleware.TimezoneMiddleware',
    'spirit.middleware.LastIPMiddleware',
    'spirit.middleware.LastSeenMiddleware',
    'spirit.middleware.ActiveUserMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'djconfig.context_processors.config',  # django-djconfig
)