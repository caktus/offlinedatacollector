from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings


@override_settings(COMPRESS_OUTPUT_DIR=settings.COMPRESS_ROOT)
class CacheManifextTestCase(TestCase):
    def test_get_page(self):
        """Audit detail"""
        with self.assertTemplateUsed('hygiene/manifest.appcache'):
            self.client.get(reverse('cache-manifest'))
