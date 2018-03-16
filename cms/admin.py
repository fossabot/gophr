import json
from django.conf import settings
from django import VERSION as django_version
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from django.utils.safestring import mark_safe

from nested_admin.nested import NestedModelAdmin, NestedStackedInline

from cms.models import Page, Section, Component, ComponentType
from cms.form import component_form_factory

def publish_page(modeladmin, request, queryset):
    queryset.update(is_published=True)
publish_page.short_description = 'Publish Page'

class ComponentInlineAdmin(NestedStackedInline):

    model = Component
    extra = 0
    # formset = inlineformset_factory(Section, Component, form=ComponentFormset, fields=('name', 'slug', 'content'))
    sortable_field_name = 'position'
    ordering = ['position']
    fields = ('component_type', 'name', 'slug', 'position', 'admin_edit_link')
    readonly_fields = ('admin_edit_link',)

    def admin_edit_link(self, obj):

        return mark_safe(obj.get_admin_edit_link())
    admin_edit_link.allow_tags = True
    admin_edit_link.short_description = "Edit Component"


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

    class Media:

        js = (
            settings.STATIC_URL + 'jquery/jquery.min.js',
            # settings.STATIC_URL + '/bootstrap/dist/js/bootstrap.min.js',
        )

        css = {
            'all': (
                settings.STATIC_URL + '/bootstrap/dist/css/bootstrap.min.css',
                settings.STATIC_URL + '/gophr-cms/css/gophr-admin.css'
            ),
        }

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
    # fields = ('section', 'component_type', 'name',)
    # readonly_fields = ('slug',)
    list_display = ('name', 'section', 'component_type',)

    def get_form(self, request, obj=None, **kwargs):

        self.obj = obj
        schema = obj.component_type.schema
        return component_form_factory(obj, json.loads(schema))

        # self.obj = obj
        # return super(ComponentAdmin, self).get_form(request, obj=obj, **kwargs)


class ComponentTypeAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug', 'is_static', 'schema')
    fields = ('name', 'slug', 'is_static', 'schema')
    readonly_fields = ('slug', 'is_static')


admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(ComponentType, ComponentTypeAdmin)
