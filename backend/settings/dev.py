from .common import *

# 끝에 추가
INSTALLED_APPS += [
    "debug_toolbar",
    'drf_yasg',
]

# 처음에 추가
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware", ] + MIDDLEWARE
#  디버그 툴바를 허용할 어드민 ip
INTERNAL_IPS = ["127.0.0.1"]

# CORS_ORIGIN_WHITELIST = ["http://localhost:3000"]
CORS_ORIGIN_ALLOW_ALL = True
