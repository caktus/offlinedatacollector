import shutil
import tempfile

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase


class TempDirectoryMixin(object):
    "Helper mixin for creating a temp directory and files inside."

    def setUp(self):
        super(TempDirectoryMixin, self).setUp()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        super(TempDirectoryMixin, self).tearDown()
        # Remove temp dir
        shutil.rmtree(self.temp_dir, ignore_errors=True)


class CacheManifextTestCase(TempDirectoryMixin, TestCase):
    def test_get_page(self):
        """Audit detail"""
        with self.assertTemplateUsed('hygiene/manifest.appcache'):
            with self.settings(LOGIN_URL=self.temp_dir):
                self.client.get(reverse('cache-manifest'))
