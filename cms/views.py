from rest_framework.viewsets import ReadOnlyModelViewSet

from cms.models import Page
from cms.serializers import PageSerializer

class PageViewSet(ReadOnlyModelViewSet):

    lookup_field = 'path'
    lookup_value_regex = '[a-z0-9\-\/]*'

    serializer_class = PageSerializer

    def get_queryset(self):


        return Page.objects.filter(is_published=True, path=self.kwargs.get('path', '/'))


    def get_object(self):

        self.kwargs['path'] = '/' + self.kwargs['path']
        return super(PageViewSet, self).get_object()
