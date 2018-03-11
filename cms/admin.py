from django import VERSION as django_version
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from nested_admin.nested import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from cms.models import Page, Section, Component, ComponentType


def publish_page(modeladmin, request, queryset):
    queryset.update(is_published=True)


publish_page.short_description = 'Publish Page'


class ComponentInlineAdmin(NestedStackedInline):

    model = Component
    extra = 1
    # sortable_field_name = ''

class SectionInlineAdmin(NestedTabularInline):

    model = Section
    can_delete = False
    fields = ('name', 'slug',)
    extra = 1
    verbose_name = 'Section for this Page'
    show_change_link = False
    inlines = [ComponentInlineAdmin]


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
    
    fields = ('section', 'component_type', 'name', 'slug')
    readonly_fields = ('slug',)

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