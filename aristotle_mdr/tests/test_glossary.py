from django.test import TestCase, Client
from aristotle_mdr import models, perms
from django.utils import timezone
from django.core.urlresolvers import reverse
from aristotle_mdr.tests import utils

from django.test.utils import setup_test_environment
setup_test_environment()

class GlossaryPage(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(GlossaryPage, self).setUp()

        # There would be too many tests to test every item type against every other
        # But they all have identical logic, so one test should suffice
        self.item1 = models.GlossaryItem.objects.create(name="Term 1",description="")
        self.item2 = models.GlossaryItem.objects.create(name="Term 2",description="")

    def test_anonymous_can_view(self):
        self.client = Client()
        response = self.client.get(reverse('aristotle:glossary'))
        self.assertEqual(response.status_code,200)
        self.assertListEqual(list(response.context['terms']),[self.item1,self.item2])
        response = self.client.get(reverse('aristotle:glossary_by_id',args=[self.item1.id]))
        self.assertEqual(response.status_code,200)
