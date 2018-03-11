from rest_framework.viewsets import ModelViewSet

from cms.models import Page
from cms.serializers import PageSerializer
from cms.config import DefaultConfig


class PageViewSet(ModelViewSet):

    lookup_field = 'path'
    lookup_value_regex = '[a-z0-9\-\/]*'

    permission_classes = DefaultConfig.default_page_permissions()
    serializer_class = PageSerializer

    def get_queryset(self):

        return Page.objects.filter(path=self.kwargs.get('path', '/'))


    def get_object(self):

        self.kwargs['path'] = '/' + self.kwargs['path']
        return super(PageViewSet, self).get_object()