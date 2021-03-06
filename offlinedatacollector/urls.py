from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from hygiene import api, views

router = DefaultRouter(trailing_slash=False)
router.register(r'cleanings', api.CleaningViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api/login/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/token/', obtain_auth_token, name='api-token'),
    url(r'^$', views.index, name='homepage'),
    url(r'^connection-test/$', views.connection_test, name='connection-test'),
    url(r'^manifest\.appcache$', views.cache_manifest, name='cache-manifest'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
