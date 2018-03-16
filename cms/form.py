import json
from collections import OrderedDict
from django.db import models
from django import forms

from cms.models import Component, ComponentType, Section

OBJ_TYPE_TO_FIELD_LOOKUP = {
    'string': {
        'field': models.CharField,
    },
    'number': {
        'field': models.FloatField
    },
    'bool': {
        'field': models.CharField
    },
    'file': {
        'field': models.FileField
    },
    'image': {
        'field': models.ImageField
    }
}

def validate_schema(schema):

    # first ensure that this is a valid schema
    fields_to_check = ('title', 'type', 'properties', 'required',)
    for field in fields_to_check:
        if field not in schema:
            raise ValueError("Invalid Schema. It must contain '%s' field." % field)

    if 'max_count' not in schema:
        schema['max_count'] = 1

    for property_name, property in schema['properties'].items():

        property_type = property['type']
        if property_type not in OBJ_TYPE_TO_FIELD_LOOKUP:
            raise ValueError("Property '%s' does not have a valid type. Given: %s. Allowed: %s" % (
                property_name, property_type, OBJ_TYPE_TO_FIELD_LOOKUP.keys()))

# def generateenerate_admin_fields(schema):
#
#     validate_schema(schema)
#     fields = [key.lower() for key in schema['properties'].keys()]
#     return (
#         ('General Information', {
#             'fields': ('section', 'component_type', 'name',)
#         }),
#         ('Component Details', {
#             'fields': tuple(fields)
#         })
#     )


def component_form_factory(component, schema):

    class BaseModel(models.Model):

        class Meta:
            abstract = True

    if type(schema) is tuple:
        schema = schema[0]
    validate_schema(schema)
    properties = schema['properties']
    required = schema['required']

    if len(properties) == 0:
        raise ValueError('This schema has no properties.')

    # now let's generate this form
    attrs = {
        '__module__': 'cms.form'
    }
    for name, property in properties.items():
        property_type = property['type']
        Field = OBJ_TYPE_TO_FIELD_LOOKUP[property_type]['field']
        attrs[name.lower()] = Field(max_length=50)

    ComponentModel = type('ComponentForAdmin', (Component,), attrs)
    form_fields = list(attrs.keys())

    class ComponentForm(forms.ModelForm):

        section = forms.ModelChoiceField(Section.objects.all())

        component_type = forms.ModelChoiceField(ComponentType.objects.all())

        name = forms.CharField(max_length=255, required=True, label='Component Name')

        class Meta:
            model = ComponentModel
            fields = form_fields

        def __init__(self, *args, **kwargs):
            self.instance = kwargs.get('instance')
            self.json_content = self.instance.content
            if self.json_content:
                self.json_content = json.loads(self.json_content)
            super(ComponentForm, self).__init__(*args, **kwargs)

            self.initial = {
                'section': self.instance.section.id,
                'component_type': self.instance.component_type.id,
                'name': self.instance.name
            }
            for name in properties.keys():
                self.initial[name.lower()] = self.json_content.get(name.lower()) if self.json_content else 'N/A'

        def save(self, commit=True):

            data = {}
            for name in properties.keys():
                data[name.lower()] = self.cleaned_data.get(name.lower())
            self.instance.content = json.dumps(data)
            self.instance.section = self.cleaned_data.get('section')
            self.instance.component_type = self.cleaned_data.get('component_type')
            self.instance.name = self.cleaned_data.get('name')
            self.instance.save()
            return self.instance

        def save_m2m(self):

            return self._save_m2m()

        def order_fields(self, field_order):

            fields = OrderedDict()
            fields['section'] = self.fields.pop('section')
            fields['component_type'] = self.fields.pop('component_type')
            fields['name'] = self.fields.pop('name')
            fields.update(self.fields)
            self.fields = fields


    return ComponentForm
