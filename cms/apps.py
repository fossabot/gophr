import logging

import django
from django.apps import AppConfig

from cms.registry import component_registry

logger = logging.getLogger('gophr')

class GophrCmsConfig(AppConfig):
    name = 'cms'
    verbose_name = 'Gophr CMS'

    def ready(self):

        ComponentType = self.get_model('ComponentType')
        component_registry.set_component_type(ComponentType)
        component_registry.auto_discover()
