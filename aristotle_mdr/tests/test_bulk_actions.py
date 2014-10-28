from django.test import TestCase, Client
from aristotle_mdr import models, perms
from django.utils import timezone
from django.core.urlresolvers import reverse
from aristotle_mdr.tests import utils

from django.test.utils import setup_test_environment
setup_test_environment()

class BulkWorkgroupActionsPage(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(BulkWorkgroupActionsPage, self).setUp()

        # There would be too many tests to test every item type against every other
        # But they all have identical logic, so one test should suffice
        self.item1 = models.ObjectClass.objects.create(name="OC1",workgroup=self.wg1)
        self.item2 = models.ObjectClass.objects.create(name="OC2",workgroup=self.wg1)
        self.item3 = models.ObjectClass.objects.create(name="OC3",workgroup=self.wg1)
        self.item4 = models.Property.objects.create(name="Prop4",workgroup=self.wg2)

    def test_bulk_favourite_on_permitted_items(self):
        self.login_editor()

        self.assertEqual(self.editor.profile.favourites.count(),0)
        response = self.client.post(reverse('aristotle:bulk_action'),
                {   'bulkaction': 'add_favourites',
                    'items'     : [self.item1.id,self.item2.id],
                }
            )
        self.assertEqual(response.status_code,302)
        self.assertEqual(self.editor.profile.favourites.count(),2)

    def test_bulk_favourite_on_forbidden_items(self):
        self.login_editor()

        self.assertEqual(self.editor.profile.favourites.count(),0)
        response = self.client.post(reverse('aristotle:bulk_action'),
                {   'bulkaction': 'add_favourites',
                    'items'     : [self.item1.id,self.item4.id],
                }
            )
        self.assertEqual(response.status_code,302)
        self.assertEqual(self.editor.profile.favourites.count(),1)

    def test_bulk_status_change_on_permitted_items(self):
        self.login_registrar()
        self.item1.readyToReview = True
        self.item2.readyToReview = True
        self.item1.save()
        self.item2.save()

        self.assertTrue(perms.user_can_change_status(self.registrar,self.item1))
        self.assertFalse(self.item1.is_registered)
        response = self.client.post(reverse('aristotle:bulk_action'),
                {   'bulkaction': 'change_state',
                    'state'     : 1,
                    'items'     : [self.item1.id,self.item2.id],
                    'registrationDate'   : "2014-10-27",
                    'cascadeRegistration': 0,
                    'registrationAuthorities'   : [self.ra.id],
                    'confirmed':'confirmed',
                }
            )
        self.assertTrue(self.item1.is_registered)
        self.assertTrue(self.item2.is_registered)

    def test_bulk_status_change_on_forbidden_items(self):
        self.login_registrar()
        self.item1.readyToReview = True
        self.item4.readyToReview = True
        self.item1.save()
        self.item4.save()

        self.assertTrue(perms.user_can_change_status(self.registrar,self.item1))
        self.assertFalse(self.item1.is_registered)
        self.assertFalse(self.item2.is_registered)
        self.assertFalse(self.item4.is_registered)
        response = self.client.post(reverse('aristotle:bulk_action'),
                {   'bulkaction': 'change_state',
                    'state'     : 1,
                    'items'     : [self.item1.id,self.item2.id,self.item4.id],
                    'registrationDate'   : "2014-10-27",
                    'cascadeRegistration': 0,
                    'registrationAuthorities'   : [self.ra.id],
                    'confirmed':'confirmed',
                }
            )
        self.assertTrue(self.item1.is_registered)
        self.assertFalse(self.item2.is_registered)
        self.assertFalse(self.item4.is_registered)
