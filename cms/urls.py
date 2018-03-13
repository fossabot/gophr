from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from cms.viewsets import PageViewSet

router = DefaultRouter()
router.register(prefix='page', viewset=PageViewSet, base_name='page')

urlpatterns = [
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^api/cms/', include(router.urls)),
]
