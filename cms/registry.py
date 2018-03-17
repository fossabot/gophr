import logging
from importlib import import_module


logger = logging.getLogger('gophr')

class ComponentExistsException(Exception):

    def __init__(self, msg, *args, **kwargs):

        self.msg = msg
        super(ComponentExistsException, self).__init__(*args, **kwargs)

class ComponentRegistry(object):

    def __init__(self):

        self.__registry = {}
        ComponentType = None

    @property
    def registry(self):

        return self.__registry

    def register(self, Component):
        from django.apps import apps

        ComponentType = apps.get_model('cms', 'ComponentType')
        component = Component()
        component_slug = component.slug

        # check that the component doesn't already exist
        if component_slug in self.registry:
            raise ComponentExistsException('Another component already exists with the same name in the codebase.')

        self.__registry[component_slug] = Component
        try:
            ct = ComponentType.objects.get(slug=component_slug)
            ct.schema = component.get_schema()
            ct.save()

        except ComponentType.DoesNotExist:
            try:
                ct = ComponentType(
                    name=Component.name,
                    slug=component_slug,
                    schema=component.get_schema()
                )
                ct.save()
            except Exception as e:
                logger.exception("Unable to create ComponentType")
        logger.info("Successfully Registered Component %s (%s)" % (component.name, component_slug))

    def set_component_type(self, ComponentType):

        ComponentType = ComponentType

    def auto_discover(self, default_module=None):

        logger.info("Begining Component Registry's AutoDiscovery Process")
        if default_module == None:
            default_module = 'components'

        from django.apps import apps

        for app_config in apps.get_app_configs():

            module_name = '%s.%s' % (app_config.name, default_module)
            try:
                import_module(module_name)
            except Exception as e:
                logger.debug("There were no components found in '%s'" % (module_name))

        logger.info("Component Registry's AutoDiscovery Ended. Successfully Registered %d components" % len(self.registry))


component_registry = ComponentRegistry()
