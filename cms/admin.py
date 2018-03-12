from django import VERSION as django_version
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from jsonschemaform.admin.widgets.jsonschema_widget import JSONSchemaWidget

from nested_admin.nested import NestedModelAdmin, NestedStackedInline

from cms.models import Page, Section, Component, ComponentType
from cms.fields import JSONTextField
from cms.forms import ComponentAdminForm
from cms.formsets import ComponentFormset
from django.forms.models import inlineformset_factory


def publish_page(modeladmin, request, queryset):
    queryset.update(is_published=True)


publish_page.short_description = 'Publish Page'
schema = {
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


class ComponentInlineAdmin(NestedStackedInline):


    model = Component
    extra = 0
    # formset = inlineformset_factory(Section, Component, form=ComponentFormset, fields=('name', 'slug', 'content'))
    sortable_field_name = 'position'
    ordering = ['position']
    fields = ('component_type', 'name', 'slug', 'position', 'get_admin_edit_link')
    readonly_fields = ('get_admin_edit_link',)
    # readonly_fields = ('slug', 'edit_component_link')

    # form = ComponentAdminForm


    # def formfield_for_dbfield(self, db_field, request, **kwargs):
    #
    #     if db_field.name == 'content':
    #         kwargs['widget'] = JSONSchemaWidget('{}')
    #     return super(ComponentInlineAdmin, self).formfield_for_dbfield(db_field, request, **kwargs)

    # readonly_fields = ('position',)
    # form = ComponentAdminForm

    # def get_formset(self, *args, **kwargs):
    #
    #     self.exclude = []
    #     obj = kwargs.get('obj')
    #     FormSet = super(ComponentInlineAdmin, self).get_formset(*args, **kwargs)
    #
    #     class ProxyFormSet(FormSet):
    #         def __init__(self, *args, **kwargs):
    #             form_kwargs = kwargs.pop('form_kwargs', {})
    #             form_kwargs['instance'] = kwargs['instance']
    #
    #             super(ProxyFormSet, self).__init__(*args, form_kwargs=form_kwargs, **kwargs)
    #
    #     return ProxyFormSet

    # def formfield_for_dbfield(self, db_field, request, **kwargs):
    #
    #     if db_field.name == ''



    # formfield_overrides = {
    #     JSONTextField: { 'widget': JSONSchemaWidget(schema) }
    # }
    # form = ComponentAdminForm
    # fields = ('name', 'component_type', 'content')
    # sortable_field_name = ''

    # @property
    # def formfield_overrides(self):

    #     import ipdb; ipdb.set_trace()

    #     schema = {}
    #     return {
    #         JSONTextField: {
    #             'widget': JSONSchemaWidget(schema)
    #         }
    #     }

    # def formfield_for_dbfield(db_field, request, **kwargs):

    #     return super(ComponentAdmin)

class SectionInlineAdmin(NestedStackedInline):

    model = Section
    can_delete = False
    fields = ('name', 'position')
    extra = 0
    verbose_name = 'Section for this Page'
    show_change_link = False
    inlines = [ComponentInlineAdmin]
    sortable_field_name = 'position'
    ordering = ['position']
    # readonly_fields = ('position',)


class PageAdmin(DraggableMPTTAdmin, NestedModelAdmin):
    mptt_level_indent = 20

    list_display = ('tree_actions', 'indented_title', 'api_url', 'path', 'created_at', 'updated_at', 'is_published')

    list_display_links = ('indented_title',)

    fields = ('site', 'name', 'title', 'description', 'is_published', 'path', 'slug')

    search_fields = ('name', 'description',)

    readonly_fields = ('path', 'slug')

    actions = [publish_page]

    actions_on_top = True

    inlines = (SectionInlineAdmin,)

    def api_url(self, obj):
        url = obj.get_absolute_url()
        if django_version[0] == 2:
            return url
        else:
            return '<a href="%s" target="_blank">%s</a>' % (url, url)
    api_url.allow_tags = True

class SectionAdmin(admin.ModelAdmin):

    list_display = ('page', 'name', 'slug')

    fields = ('page', 'name', 'slug')
    readonly_fields = ('slug',)

class ComponentAdmin(admin.ModelAdmin):

    list_display = ('section', 'component_type', 'name', 'slug')

    fields = ('section', 'component_type', 'name', 'slug', 'content')
    readonly_fields = ('slug',)
    list_display = ('name', 'section', 'component_type', 'slug')

    class Media:


        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
        )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        schema = {
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

        if db_field.name == 'content':
            import json
            # kwargs['widget'] = JSONSchemaWidget(json.dumps(self.obj.component_type.schema))
            kwargs['widget'] = JSONSchemaWidget(schema)

        return super(ComponentAdmin, self).formfield_for_dbfield(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):

        self.obj = obj
        return super(ComponentAdmin, self).get_form(request, obj=obj, **kwargs)

class ComponentTypeAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug', 'is_static', 'schema')
    fields = ('name', 'slug', 'is_static', 'schema')
    readonly_fields = ('slug', 'is_static')


# class SectionAdmin(admin.ModelAdmin):

#     list_display = ('name', 'slug', 'resource')

#     @property
#     def inlines(self):

#         inlines = []
#         for component_name, component in component_registry.components.items():

#             class_name = "%sAdmin" % component_name.replace(' ', '')
#             InlineAdmin = type(class_name, (admin.TabularInline,), {
#                 'model': component,
#                 'can_delete': False,
#                 'extra': 1,
#                 'show_change_link': True,
#             })
#             inlines.append(InlineAdmin)
#         return tuple(inlines)




admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(ComponentType, ComponentTypeAdmin)
