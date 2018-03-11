from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from cms.viewsets import PageViewSet

router = DefaultRouter()
router.register(prefix='page', viewset=PageViewSet, base_name='page')

urlpatterns = router.urls
