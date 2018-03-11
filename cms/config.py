from django.conf import settings

from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from cms.permissions import PagePermission

class DefaultConfig(object):

    @classmethod
    def default_page_permissions(cls):

        return (PagePermission, DjangoModelPermissionsOrAnonReadOnly,)
