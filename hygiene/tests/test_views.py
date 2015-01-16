import os
import shutil
import tempfile

from django.core.urlresolvers import reverse
from django.test import TestCase


class TempDirectoryMixin(object):
    "Helper mixin for creating a temp directory and files inside."

    def setUp(self):
        super(TempDirectoryMixin, self).setUp()
        self.temp_dir = tempfile.mkdtemp()
        os.mkdir(os.path.join(self.temp_dir, 'CACHE'))

    def tearDown(self):
        super(TempDirectoryMixin, self).tearDown()
        # Remove temp dir
        shutil.rmtree(self.temp_dir, ignore_errors=True)


class CacheManifextTestCase(TempDirectoryMixin, TestCase):
    def test_get_page(self):
        with self.assertTemplateUsed('hygiene/manifest.appcache'):
            with self.settings(COMPRESS_ROOT=self.temp_dir):
                response = self.client.get(reverse('cache-manifest'))
                self.assertEqual(200, response.status_code)
                self.assertEqual('text/cache-manifest', response['Content-Type'])
