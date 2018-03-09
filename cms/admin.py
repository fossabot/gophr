from django import VERSION as django_version
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from cms.models import Page, component_registry, Section


def publish_page(modeladmin, request, queryset):
    queryset.update(is_published=True)


publish_page.short_description = 'Publish Page'


class SectionInlineAdmin(admin.TabularInline):

    model = Section
    can_delete = False
    fields = ('name', 'slug',)
    extra = 1
    verbose_name = 'Section for this Page'
    show_change_link = False


class PageAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20

    list_display = ('tree_actions', 'indented_title', 'api_url', 'path', 'created_at', 'updated_at', 'is_published')

    list_display_links = ('indented_title',)

    search_fields = ('name', 'description',)

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

    list_display = ('name', 'slug', 'resource')

    @property
    def inlines(self):

        inlines = []
        for component_name, component in component_registry.components.items():

            class_name = "%sAdmin" % component_name.replace(' ', '')
            InlineAdmin = type(class_name, (admin.TabularInline,), {
                'model': component,
                'can_delete': False,
                'extra': 1,
                'show_change_link': True,
            })
            inlines.append(InlineAdmin)
        return tuple(inlines)

    


admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)