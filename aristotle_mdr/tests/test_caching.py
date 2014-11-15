from django.test import TestCase

import aristotle_mdr.models as models
import aristotle_mdr.perms as perms
import aristotle_mdr.tests.utils as utils
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import datetime
from time import sleep

from django.test.utils import setup_test_environment
setup_test_environment()

class CachingForRawPermissions(TestCase):

    def setUp(self):
        self.ra = models.RegistrationAuthority.objects.create(name="Test RA")
        self.wg = models.Workgroup.objects.create(name="Test WG 1")
        self.wg.registrationAuthorities=[self.ra]
        self.wg.save()
        self.submitter = User.objects.create_user('suzie','','submitter')
        self.wg.submitters.add(self.submitter)
        self.item = models.ObjectClass.objects.create(name="Test OC1",workgroup=self.wg)

    def test_can_edit_cache(self):
        self.assertTrue(perms.user_can_edit(self.submitter,self.item))
        self.item.description = "edit name, then quickly check permission"
        self.item.save()
        self.assertTrue(perms.user_can_edit(self.submitter,self.item))
        self.item.description = "edit name, then wait 30 secs for 'recently edited to expire'"
        self.item.save()
        sleep(models.VERY_RECENTLY_SECONDS+2)
        self.assertTrue(perms.user_can_edit(self.submitter,self.item))
        # register then immediately check the permissions to make sure the cache is ignored
        # technically we haven't edited the item yet, although ``concept.recache_states`` might be called.
        reg,c = models.Status.objects.get_or_create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate = datetime.date(2009,04,28),
            state =  models.STATES.standard
            )
        self.assertFalse(perms.user_can_edit(self.submitter,self.item))

    def test_can_view_cache(self):
        self.viewer = User.objects.create_user('vicky','','viewer') # Don't need to assign any workgroups

        self.assertTrue(perms.user_can_view(self.submitter,self.item))
        self.assertFalse(perms.user_can_view(self.viewer,self.item))
        self.item.description = "edit name, then quickly check permission"
        self.item.save()
        self.assertTrue(perms.user_can_view(self.submitter,self.item))
        self.assertFalse(perms.user_can_view(self.viewer,self.item))
        self.item.description = "edit name, then wait 30 secs for 'recently edited to expire'"
        self.item.save()
        sleep(models.VERY_RECENTLY_SECONDS+2)
        self.assertTrue(perms.user_can_view(self.submitter,self.item))
        self.assertFalse(perms.user_can_view(self.viewer,self.item))
        # register then immediately check the permissions to make sure the cache is ignored
        # technically we haven't edited the item yet, although ``concept.recache_states`` might be called.
        reg,c = models.Status.objects.get_or_create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate = datetime.date(2009,04,28),
            state =  models.STATES.standard
            )
        self.assertTrue(perms.user_can_view(self.submitter,self.item))
        self.assertTrue(perms.user_can_view(self.viewer,self.item))

"""
class TestPageViewCaches(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(TestPageViewCaches, self).setUp()
        self.viewer2 = User.objects.create_user('viewer2','','viewer') # not in any workgroup
        self.viewer3 = User.objects.create_user('viewer3','','viewer') # not in our "primary testing workgroup" (self.wg1)
        self.wg1.giveRoleToUser('viewer',self.viewer3)
        self.wg2 = models.Workgroup.objects.create(name="Test WG 2")

    def can_the_current_logged_in_user_post(self):
        pass
"""