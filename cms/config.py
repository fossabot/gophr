from django.conf import settings

DEFAULT_cms = {
    'MODELS' : {
        'RESOURCE': {
            'NAME': {
                'LENGTH': 255,
                'REQUIRED': True,
                'BLANK': False
            },
            'DESCRIPTION': {
                'LENGTH': 500,
                'REQUIRED': False,
                'BLANK': True
            },
            'SLUG': {
                'LENGTH': 255,
                'REQUIRED': True,
                'BLANK': True
            },
        },
        'PAGE': {
            'TITLE': {
                'LENGTH': 255,
                'REQUIRED': False,
                'BLANK': True
            }
        },
        'SECTION': {
            'RESOURCE': {
                'FOREIGN_KEY': 'cms.Page'
            },
            'NAME': {
                'LENGTH': 255,
                'REQUIRED': True,
                'BLANK': False
            },
            'SLUG': {
                'LENGTH': 255,
                'REQUIRED': True,
                'BLANK': True
            }
        },
        'COMPONENT': {
            'NAME': {
                'LENGTH': 255,
                'REQUIRED': True,
                'BLANK': False
            },
            'SLUG': {
                'LENGTH': 255,
                'REQUIRED': True,
                'BLANK': True
            }
        }
    }
}

class Configuration(object):

    def __init__(self):

        config = getattr(settings, 'cms', DEFAULT_cms)
        self.__dict__ = config

    @property
    def resource_name_config(self):
        
        return self.MODELS.get('RESOURCE', {}).get('NAME', {})

    @property
    def resource_description_config(self):

        return self.MODELS.get('RESOURCE', {}).get('DESCRIPTION', {})

    @property
    def resource_slug_config(self):

        return self.MODELS.get('RESOURCE', {}).get('SLUG', {})

    @property
    def page_title_config(self):

        return self.MODELS.get('PAGE', {}).get('TITLE', {})

    @property
    def section_resource_config(self):

        return self.MODELS.get('SECTION', {}).get('RESOURCE', {})

    @property
    def section_name_config(self):
        return self.MODELS.get('SECTION', {}).get('NAME', {})

    @property
    def section_slug_config(self):

        return self.MODELS.get('SECTION', {}).get('SLUG', {})

    @property
    def component_name_config(self):
        return self.MODELS.get('COMPONENT', {}).get('NAME', {})

    @property
    def component_slug_config(self):
        return self.MODELS.get('COMPONENT', {}).get('SLUG', {})

configuration = Configuration()