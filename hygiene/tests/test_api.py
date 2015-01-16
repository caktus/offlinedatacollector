import datetime

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .. import models
from . import factories


class CleaningAPITestCase(APITestCase):

    def setUp(self):
        super().setUp()
        self.user = factories.UserFactory.create()
        self.url = reverse('cleaning-list')
        self.client.force_authenticate(user=self.user)

    def assertResultsEqual(self, response, expected):
        """Assert results listed in the response."""
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = sorted(map(lambda x: x.pk, expected))
        found = sorted(map(lambda x: x['id'], response.data['results']))
        self.assertEqual(found, expected)

    def test_browse(self):
        """Read cleanings. Can only see their own records."""

        cleaning = factories.CleaningFactory.create(user=self.user)
        factories.CleaningFactory.create()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = [cleaning.pk, ]
        found = sorted(map(lambda x: x['id'], response.data['results']))
        self.assertEqual(found, expected)

    def test_read(self):
        """View a single cleaning. Can only see their own records."""

        cleaning = factories.CleaningFactory.create(user=self.user)
        url = reverse('cleaning-detail', kwargs={'pk': cleaning.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        other = factories.CleaningFactory.create()
        url = reverse('cleaning-detail', kwargs={'pk': other.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit(self):
        """Edit cleaning record."""

        cleaning = factories.CleaningFactory.create(user=self.user)
        url = reverse('cleaning-detail', kwargs={'pk': cleaning.pk})
        data = {
            'completed': False,
            'date': cleaning.date.isoformat(),
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_duplicate(self):
        """Cannot edit a record to create a duplicate."""

        cleaning = factories.CleaningFactory.create(user=self.user)
        other = factories.CleaningFactory.create(user=self.user)
        url = reverse('cleaning-detail', kwargs={'pk': cleaning.pk})
        data = {
            'completed': False,
            'date': other.date.isoformat(),
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add(self):
        """Add new cleaning record."""

        data = {
            'completed': False,
            'date': datetime.date.today().isoformat(),
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cleaning = models.Cleaning.objects.latest('pk')
        self.assertEqual(cleaning.user, self.user)
        self.assertEqual(cleaning.date, datetime.date.today())
        self.assertFalse(cleaning.completed)

    def test_add_duplicate(self):
        """Attempt to add a duplicate record: same date and user."""

        cleaning = factories.CleaningFactory.create(user=self.user)
        data = {
            'completed': False,
            'date': cleaning.date.isoformat(),
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        """Delete cleaning record."""

        cleaning = factories.CleaningFactory.create(user=self.user)
        url = reverse('cleaning-detail', kwargs={'pk': cleaning.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(models.Cleaning.DoesNotExist):
            models.Cleaning.objects.get(pk=cleaning.pk)
