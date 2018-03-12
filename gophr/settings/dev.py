from .base import *

SITE_ID = 1

# SECURITY WARNING: keep the debug value as False in production!
# BE SURE TO OVERRIDE THIS FROM BASE AND SET IT TO FALSE
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# BE SURE TO OVERRIDE THIS IN PRODUCTION!
SECRET_KEY = '!s*jz&g_%%vtgvr@49!qopp_qw%jolj_nbf@125o1l$#zbln=w'

INSTALLED_APPS.append('cms')
INSTALLED_APPS.append('mptt')
INSTALLED_APPS.append('nested_admin')
INSTALLED_APPS.append('jsonschemaform')