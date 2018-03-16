import json

from django.utils.text import slugify

from registry import component_registry


class BaseComponent(object):
    '''

    NOTE: Once a Component gets a name, and it is registered, we recommend that you not change the name,
    because it will be the name that will be used in the database for the lifetime of the application.
    '''
    name = None

    @property
    def slug(self):
        '''
        Generates the Slug for this component.
        '''
        return slugify(self.name)

    def get_schema(self):
        '''
        Returns the Schema for this Component.
        '''
        raise NotImplementedError()


class QuoteComponent(BaseComponent):

    name = 'Quotes'

    def get_schema(self):

        return json.dumps({
            "title": "Quote",
            "type": "object",
            "properties": {
                "quote": {"type": "string"},
                "attribution": {"type": "string"}
            },
            "required": ["quote", "attribution"]
        })


class Card(BaseComponent):

    name = 'Card'

    def get_schema(self):

        return json.dumps({
            "title": "Quote",
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "link": { "type": "string" }
            },
            "required": ["title",]
        })

component_registry.register(QuoteComponent)
component_registry.register(Card)
