from django.core.urlresolvers import reverse
from django.test import TestCase


class CacheManifextTestCase(TestCase):
    def test_get_page(self):
        """Audit detail"""
        with self.assertTemplateUsed('hygiene/manifest.appcache'):
            self.client.get(reverse('cache-manifest'))
