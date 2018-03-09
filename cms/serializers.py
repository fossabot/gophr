from django.forms.models import model_to_dict
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from cms.models import Page


PAGE_FIELDS = ('name', 'slug', 'description', 'is_published', 'parent', 'path', 'get_absolute_url', 'created_at', 'updated_at', )

class PageSerializer(ModelSerializer):

    parent = SerializerMethodField()
    children = SerializerMethodField()

    class Meta:

        model = Page
        fields = ('name', 'slug', 'description', 'is_published', 'path', 'parent', 'children', 'get_absolute_url', 'created_at', 'updated_at', )

    def __get_page_attributes(self, page):

        if page:
            return {
                'name': page.name,
                'slug': page.slug,
                'description': page.description,
                'is_published': page.is_published,
                'path': page.path,
                'get_absolute_url': page.get_absolute_url(),
                'created_at': page.created_at,
                'updated_at': page.updated_at,
            }
        else:
            return []

    def get_children(self, obj):

        children = []
        for c in obj.get_children():
            children.append(self.__get_page_attributes(c))
        return children

    def get_parent(self, obj):

        if obj.parent:
            return self.__get_page_attributes(obj.parent)
        else:
            return []
