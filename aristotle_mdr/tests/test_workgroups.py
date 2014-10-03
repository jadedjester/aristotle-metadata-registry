from django.test import TestCase, Client
from aristotle_mdr import models, perms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse
from aristotle_mdr.tests import utils

from django.test.utils import setup_test_environment
setup_test_environment()

#This is for testing permissions around workgroup mangement.

class WorkgroupMembership(TestCase):
    def test_userInWorkgroup(self):
        wg = models.Workgroup.objects.create(name="Test WG 1")
        user = User.objects.create_user('editor1','','editor1')
        wg.addUser(user)
        self.assertTrue(perms.user_in_workgroup(user,wg))
    def test_RemoveUserFromWorkgroup(self):
        #Does removing a user from a workgroup remove their permissions? It should!
        wg = models.Workgroup.objects.create(name="Test WG 1")
        user = User.objects.create_user('editor1','','editor1')
        wg.addUser(user)
        wg.giveRoleToUser("Manager",user)
        # Caching issue, refresh from DB with correct permissions
        user = User.objects.get(pk=user.pk)
        self.assertTrue(perms.user_in_workgroup(user,wg))
        self.assertTrue(perms.user_is_workgroup_manager(user,wg))
        wg.removeUser(user)
        # Caching issue, refresh from DB with correct permissions
        user = User.objects.get(pk=user.pk)
        self.assertFalse(perms.user_is_workgroup_manager(user,wg))
    def test_managersCanEditWorkgroups(self):
        wg = models.Workgroup.objects.create(name="Test WG 1")
        user1 = User.objects.create_user('manager','','manager')
        user2 = User.objects.create_user('editor','','editor')
        wg.addUser(user1)
        wg.addUser(user2)
        wg.giveRoleToUser("Manager",user1)
        wg.giveRoleToUser("Viewer",user2)

        # Caching issue, refresh from DB with correct permissions
        self.assertTrue(perms.user_in_workgroup(user1,wg))
        self.assertTrue(perms.user_in_workgroup(user2,wg))
        self.assertTrue(perms.user_can_view(user2,wg))
        self.assertTrue(perms.user_can_view(user1,wg))

        self.assertTrue(perms.user_can_edit(user1,wg))
        self.assertFalse(perms.user_can_edit(user2,wg))
        wg.removeUser(user1)
        wg.removeUser(user2)
        # Caching issue, refresh from DB with correct permissions
        user1 = User.objects.get(pk=user1.pk)
        user2 = User.objects.get(pk=user2.pk)
        self.assertFalse(perms.user_can_edit(user1,wg))
        self.assertFalse(perms.user_can_edit(user2,wg))

class WorkgroupAnonTests(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(WorkgroupAnonTests, self).setUp()
        self.newuser = User.objects.create_user('nathan','','noobie')
        self.newuser.save()

    def test_anon_cannot_add(self):
        self.logout()
        response = self.client.get(reverse('aristotle:addWorkgroupMembers',args=[self.wg1.id]))
        self.assertRedirects(response,
            reverse("django.contrib.auth.views.login",)+"?next="+
            reverse('aristotle:addWorkgroupMembers',args=[self.wg1.id])
            )

        response = self.client.get(reverse('aristotle:removeWorkgroupRole',args=[self.wg1.id,'Viewer',self.newuser.pk]))
        self.assertRedirects(response,
            reverse("django.contrib.auth.views.login",)+"?next="+
            reverse('aristotle:removeWorkgroupRole',args=[self.wg1.id,'Viewer',self.newuser.pk])
            )

        response = self.client.post(
            reverse('aristotle:addWorkgroupMembers',args=[self.wg1.id]),
            {'roles':['Viewer'],
             'users':[self.newuser.pk]
            })
        self.assertRedirects(response,
            reverse("django.contrib.auth.views.login",)+"?next="+
            reverse('aristotle:addWorkgroupMembers',args=[self.wg1.id])
            )
        self.assertListEqual(list(self.newuser.profile.workgroups.all()),[])


class WorkgroupMemberTests(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(WorkgroupMemberTests, self).setUp()
        self.newuser = User.objects.create_user('nathan','','noobie')
        self.newuser.save()

    def test_viewer_cannot_add_or_remove_users(self):
        self.login_viewer()
        response = self.client.get(reverse('aristotle:addWorkgroupMembers',args=[self.wg1.id]))
        self.assertEqual(response.status_code,302)
        response = self.client.get(reverse('aristotle:removeWorkgroupRole',args=[self.wg1.id,'Viewer',self.newuser.pk]))
        self.assertEqual(response.status_code,302)

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

