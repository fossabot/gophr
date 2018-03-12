from cms.models import Component
from jsonschemaform.admin.widgets.jsonschema_widget import JSONSchemaWidget

from django import forms

class ComponentAdminForm(forms.ModelForm):

    class Meta:

        model = Component
        fields = ('section', 'component_type', 'name', 'slug', 'content',)

    def __init__(self, *args, **kwargs):

        form = super(ComponentAdminForm, self).__init__(*args, **kwargs)
        # print('>>> instance', kwargs['instance'])

        default_schema = schema = {
            "title": "Config Schema",
            "description": "My configutation schema",
            "type": "object",
            "properties": {
                "columns": {
                    "description": "List of columns size",
                    "type": "array"
                },
                "class": {
                    "description": "A reference css class",
                    "type": "string"
                },
                "container": {
                    "default": "container",
                    "description": "Default page container",
                    "type": "string"
                }
            },
            "required": [
                "columns",
            ],
        }
        component_type = self.fields['component_type']
        print("Content Type: %s" % str(component_type))
        print("Args: %s" % str(args))
        print("KWargs: %s" % str(kwargs))
        return form
        # if component_type:
        # self.fields['content'].widget = JSONSchemaWidget(component_type.schema)
