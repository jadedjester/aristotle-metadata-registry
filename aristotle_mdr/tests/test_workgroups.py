from django.test import TestCase, Client
from aristotle_mdr import models, perms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse
from aristotle_mdr.tests import utils

from django.test.utils import setup_test_environment
setup_test_environment()
import unittest

#This is for testing permissions around workgroup mangement.

class WorkgroupMemberTests(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(WorkgroupMemberTests, self).setUp()
        self.newuser = User.objects.create_user('nathan','','noobie')
        self.newuser.save()

    def test_viewer_cannot_add_or_remove_users(self):
        self.login_viewer()
        response = self.client.get(reverse('aristotle:addWorkgroupMembers',args=[self.wg1.id]))
        self.assertEqual(response.status_code,403)

    def test_manager_can_add_or_remove_users(self):
        self.login_manager()
        self.assertTrue(self.newuser in list(User.objects.all()))

        response = self.client.get(reverse('aristotle:addWorkgroupMembers',args=[self.wg2.id]))
        self.assertEqual(response.status_code,403)
        response = self.client.get(reverse('aristotle:addWorkgroupMembers',args=[self.wg1.id]))
        self.assertEqual(response.status_code,200)
        self.assertTrue(self.newuser.id in [u[0] for u in response.context['form'].fields['users'].choices])

        self.assertListEqual(list(self.newuser.profile.workgroups.all()),[])
        response = self.client.post(
            reverse('aristotle:addWorkgroupMembers',args=[self.wg2.id]),
            {'roles':['Viewer'],
             'users':[self.newuser.pk]
            })
        self.assertEqual(response.status_code,403)
        self.assertListEqual(list(self.newuser.profile.workgroups.all()),[])

        response = self.client.post(
            reverse('aristotle:addWorkgroupMembers',args=[self.wg1.id]),
            {'roles':['Viewer'],
             'users':[self.newuser.pk]
            })
        self.assertEqual(response.status_code,302)
        self.assertTrue(self.newuser.profile in self.wg1.members.all())
        self.assertListEqual(list(self.newuser.profile.workgroups.all()),[self.wg1])

        response = self.client.get(reverse('aristotle:removeWorkgroupRole',args=[self.wg1.id,'Viewer',self.newuser.pk]))
        self.assertEqual(response.status_code,302)
        self.assertFalse(self.newuser.profile in self.wg1.viewers.all())
        response = self.client.get(reverse('aristotle:removeWorkgroupRole',args=[self.wg1.id,'Viewer',self.newuser.pk]))
        self.assertEqual(response.status_code,302)
        self.assertFalse(self.newuser.profile in self.wg1.viewers.all())
        #removeWorkgroupRole

