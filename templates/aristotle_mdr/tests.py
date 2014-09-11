from django.test import TestCase, Client
from aristotle_mdr import models, perms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission

from django.test.utils import setup_test_environment
setup_test_environment()

#  Create your tests here.

class SuperuserPermissions(TestCase):
    # All of the below are called with None as a Superuser, by definition *must* be able to edit, view and managed everything. Since a is_superuser chcek is cheap is should be called first, so calling with None checks that there is no other database calls going on.

    def test_can_view(self):
        s = User.objects.create_superuser('super','','user')
        self.assertTrue(perms.user_can_view(s,None))
    def test_is_registrar(self):
        s = User.objects.create_superuser('super','','user')
        self.assertTrue(perms.user_is_registrar(s))
    def test_is_registrar_in_ra(self):
        s = User.objects.create_superuser('super','','user')
        self.assertTrue(perms.user_is_registrar_in_ra(s,None))
    def test_is_workgroup_manager(self):
        s = User.objects.create_superuser('super','','user')
        self.assertTrue(perms.user_is_workgroup_manager(s,None))
    def test_can_change_status(self):
        s = User.objects.create_superuser('super','','user')
        self.assertTrue(perms.user_can_change_status(s,None))
    def test_can_edit(self):
        s = User.objects.create_superuser('super','','user')
        self.assertTrue(perms.user_can_edit(s,None))
    def test_in_workgroup(self):
        s = User.objects.create_superuser('super','','user')
        self.assertTrue(perms.user_in_workgroup(s,None))

# Since all managed objects have the same rules, these can be used to cover everything
# This isn't an actual TestCase, we'll just pretend it is
class ManagedObjectVisibility(object):
    def test_object_is_public(self):
        ra = models.RegistrationAuthority.objects.create(name="Test RA")
        self.wg = models.Workgroup.objects.create(name="Test WG")

        self.assertEqual(self.item.is_public(),False)
        s = models.Status.objects.create(
                concept=self.item,
                registrationAuthority=ra,
                registrationDate=timezone.now(),
                state=ra.public_state
                )
        self.assertEqual(s.registrationAuthority,ra)
        self.assertEqual(self.item.is_public(),True)
        ra.public_state = models.STATES.standard
        ra.save()
        self.assertEqual(self.item.is_public(),False)
        self.item.statuses.first().state = models.STATES.standard
        self.item.save()
        self.assertEqual(self.item.is_public(),False)

    def test_registrar_can_view(self):
        # set up
        ra = models.RegistrationAuthority.objects.create(name="Test RA")

        # make editor for wg1
        r1 = User.objects.create_user('reg','','reg')

        self.assertEqual(perms.user_can_view(r1,self.item),False)
        s = models.Status.objects.create(
                concept=self.item,
                registrationAuthority=ra,
                registrationDate=timezone.now(),
                state=ra.locked_state
                )
        self.assertEqual(perms.user_can_view(r1,self.item),False)
        # Caching issue, refresh from DB with correct permissions
        ra.giveRoleToUser('Registrar',r1)
        r1 = User.objects.get(pk=r1.pk)

        self.assertEqual(perms.user_can_view(r1,self.item),True)


    def test_object_editor_can_view(self):
        # set up
        ra = models.RegistrationAuthority.objects.create(name="Test RA")

        # make editor for wg1
        wg1 = models.Workgroup.objects.create(name="Test WG 1")
        e1 = User.objects.create_user('editor1','','editor1')
        wg1.giveRoleToUser('Editor',e1)

        # make editor for wg2
        wg2 = models.Workgroup.objects.create(name="Test WG 2")
        e2 = User.objects.create_user('editor2','','editor2')
        wg2.giveRoleToUser('Editor',e2)

        # make an Object Class in wg1
        oc = self.item
        self.item.workgroup = wg1
        self.item.save()

        # test editor 1 can view, editor 2 cannot
        self.assertEqual(perms.user_can_view(e1,self.item),True)
        self.assertEqual(perms.user_can_view(e2,self.item),False)

        # move Object Class to wg2
        self.item.workgroup = wg2
        self.item.save()

        # test editor 2 can view, editor 1 cannot
        self.assertEqual(perms.user_can_view(e2,self.item),True)
        self.assertEqual(perms.user_can_view(e1,self.item),False)

        s = models.Status.objects.create(
                concept=self.item,
                registrationAuthority=ra,
                registrationDate=timezone.now(),
                state=ra.locked_state
                )
        # Editor 2 can view. Editor 1 cannot
        self.assertEqual(perms.user_can_view(e2,self.item),True)
        self.assertEqual(perms.user_can_view(e1,self.item),False)

        # Set status to a public state
        s.state = ra.public_state
        s.save()
        # Both can view, neither can edit.
        self.assertEqual(perms.user_can_view(e1,self.item),True)
        self.assertEqual(perms.user_can_view(e2,self.item),True)

    def test_object_editor_can_edit(self):
        # set up
        ra = models.RegistrationAuthority.objects.create(name="Test RA")

        # make editor for wg1
        wg1 = models.Workgroup.objects.create(name="Test WG 1")
        e1 = User.objects.create_user('editor1','','editor1')
        wg1.giveRoleToUser('Editor',e1)

        # make editor for wg2
        wg2 = models.Workgroup.objects.create(name="Test WG 2")
        e2 = User.objects.create_user('editor2','','editor2')
        wg2.giveRoleToUser('Editor',e2)

        # make an Object Class in wg1
        oc = self.item
        self.item.workgroup = wg1
        self.item.save()

        # test editor 1 can edit, editor 2 cannot
        self.assertEqual(perms.user_can_edit(e1,self.item),True)
        self.assertEqual(perms.user_can_edit(e2,self.item),False)

        # move Object Class to wg2
        self.item.workgroup = wg2
        self.item.save()

        # test editor 2 can edit, editor 1 cannot
        self.assertEqual(perms.user_can_edit(e2,self.item),True)
        self.assertEqual(perms.user_can_edit(e1,self.item),False)

        s = models.Status.objects.create(
                concept=self.item,
                registrationAuthority=ra,
                registrationDate=timezone.now(),
                state=ra.locked_state
                )
        # Editor 2 can no longer edit. Neither can Editor 1
        self.assertEqual(perms.user_can_edit(e2,self.item),False)
        self.assertEqual(perms.user_can_view(e1,self.item),False)

class ObjectClassVisibility(TestCase,ManagedObjectVisibility):
    def setUp(self):
        self.wg = models.Workgroup.objects.create(name="Setup WG")
        self.item = models.ObjectClass.objects.create(name="Test OC",workgroup=self.wg)
class PropertyVisibility(TestCase,ManagedObjectVisibility):
    def setUp(self):
        self.wg = models.Workgroup.objects.create(name="Setup WG")
        self.item = models.Property.objects.create(name="Test P",workgroup=self.wg)
class ValueDomainVisibility(TestCase,ManagedObjectVisibility):
    def setUp(self):
        self.wg = models.Workgroup.objects.create(name="Setup WG")
        self.item = models.ValueDomain.objects.create(name="Test VD",
                workgroup=self.wg,
                format = "X" ,
                maximumLength = 3,
                dataType = models.DataType.objects.create(name="Test DT",workgroup=self.wg)
                )
class DataElementConceptVisibility(TestCase,ManagedObjectVisibility):
    def setUp(self):
        self.wg = models.Workgroup.objects.create(name="Setup WG")
        self.item = models.DataElementConcept.objects.create(name="Test DEC",
            workgroup=self.wg,
            )
class DataElementVisibility(TestCase,ManagedObjectVisibility):
    def setUp(self):
        self.wg = models.Workgroup.objects.create(name="Setup WG")
        self.item = models.DataElement.objects.create(name="Test DE",
            workgroup=self.wg,
            )
class DataTypeVisibility(TestCase,ManagedObjectVisibility):
    def setUp(self):
        self.wg = models.Workgroup.objects.create(name="Setup WG")
        self.item = models.DataType.objects.create(name="Test DT",
            workgroup=self.wg,
            )
class PackageVisibility(TestCase,ManagedObjectVisibility):
    def setUp(self):
        self.wg = models.Workgroup.objects.create(name="Setup WG")
        self.item = models.Package.objects.create(name="Test Package",
            workgroup=self.wg,
            )

class RegistryGroupPermissions(TestCase):
    def test_RegistrationAuthority_name_change(self):
        ra = models.RegistrationAuthority.objects.create(name="Test RA")
        user = User.objects.create_user('registrar','','registrar')

        # User isn't in RA... yet
        self.assertFalse(perms.user_is_registrar_in_ra(user,ra))

        # Add user to RA, assert user is in RA
        ra.giveRoleToUser('Registrar',user)
        # Caching issue, refresh from DB with correct permissions
        user = User.objects.get(pk=user.pk)
        self.assertTrue(perms.user_is_registrar_in_ra(user,ra))

        # Change name of RA, assert user is still in RA
        ra.name = "Test RA2"
        ra.save()
        user = User.objects.get(pk=user.pk)
        self.assertTrue(perms.user_is_registrar_in_ra(user,ra))

        # Add new RA with old RA's name, assert user is not in the new RA
        newRA = models.RegistrationAuthority.objects.create(name="Test RA")
        user = User.objects.get(pk=user.pk)
        self.assertFalse(perms.user_is_registrar_in_ra(user,newRA))

        # Remove user to RA, assert user is no longer in RA
        ra.removeRoleFromUser('Registrar',user)
        # Caching issue, refresh from DB with correct permissions
        user = User.objects.get(pk=user.pk)
        self.assertFalse(perms.user_is_registrar_in_ra(user,ra))

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
        user1 = User.objects.get(pk=user1.pk)
        user2 = User.objects.get(pk=user2.pk)
        self.assertTrue(perms.user_in_workgroup(user1,wg))
        self.assertTrue(perms.user_in_workgroup(user2,wg))
        self.assertTrue(perms.user_can_edit(user1,wg))
        self.assertFalse(perms.user_can_edit(user2,wg))
        wg.removeUser(user1)
        wg.removeUser(user2)
        # Caching issue, refresh from DB with correct permissions
        user1 = User.objects.get(pk=user1.pk)
        user2 = User.objects.get(pk=user2.pk)
        self.assertFalse(perms.user_can_edit(user1,wg))
        self.assertFalse(perms.user_can_edit(user2,wg))

class UserEditTesting(TestCase):
    def test_canViewProfile(self):
        u1 = User.objects.create_user('user1','','user1')
        u2 = User.objects.create_user('user2','','user2')
        self.assertFalse(perms.user_can_view(u1,u2))
        self.assertFalse(perms.user_can_view(u2,u1))
        self.assertTrue(perms.user_can_view(u1,u1))
        self.assertTrue(perms.user_can_view(u2,u2))
    def test_canEditProfile(self):
        u1 = User.objects.create_user('user1','','user1')
        u2 = User.objects.create_user('user2','','user2')
        self.assertFalse(perms.user_can_edit(u1,u2))
        self.assertFalse(perms.user_can_edit(u2,u1))
        self.assertTrue(perms.user_can_edit(u1,u1))
        self.assertTrue(perms.user_can_edit(u2,u2))

class AnonymousUserViewingThePages(TestCase):
    def setUp(self):
        self.client = Client()
    def test_homepage(self):
        home = self.client.get("/")
        self.assertEqual(home.status_code,200)
    def test_visible_item(self):
        wg = models.Workgroup.objects.create(name="Setup WG")
        ra = models.RegistrationAuthority.objects.create(name="Test RA")
        item = models.ObjectClass.objects.create(name="Test OC",workgroup=wg)
        s = models.Status.objects.create(
                concept=item,
                registrationAuthority=ra,
                registrationDate=timezone.now(),
                state=ra.locked_state
                )
        home = self.client.get("/item/%s"%item.id)
        #Anonymous users requesting a hidden page will be redirected to login
        self.assertEqual(home.status_code,302)
        s.state = ra.public_state
        s.save()
        home = self.client.get("/item/%s"%item.id)
        self.assertEqual(home.status_code,200)

class CustomQuerySetTest(TestCase):
    def test_is_public(self):
        ra = models.RegistrationAuthority.objects.create(name="Test RA",public_state=models.STATES.standard)
        wg = models.Workgroup.objects.create(name="Setup WG")
        oc1 = models.ObjectClass.objects.create(name="Test OC1",workgroup=wg)
        oc2 = models.ObjectClass.objects.create(name="Test OC2",workgroup=wg)
        user = User.objects.create_superuser('super','','user')

        # Assert no public items
        self.assertEqual(len(models.ObjectClass.objects.all().public()),0)

        # Register OC1 only
        ra.register(oc1,models.STATES.standard,user)

        # Assert only OC1 is public
        self.assertEqual(len(models.ObjectClass.objects.all().public()),1)
        self.assertTrue(oc1 in models.ObjectClass.objects.all().public())
        self.assertTrue(oc2 not in models.ObjectClass.objects.all().public())

        # Deregister OC1
        state=models.STATES.incomplete
        ra.register(oc1,state,user)

        # Assert no public items
        self.assertEqual(len(models.ObjectClass.objects.all().public()),0)

class RegistryCascadeTest(TestCase):
    def test_DataElementConceptCascade(self):
        user = User.objects.create_superuser('super','','user')
        self.ra = models.RegistrationAuthority.objects.create(name="Test RA")
        self.wg = models.Workgroup.objects.create(name="Setup WG")
        self.oc = models.ObjectClass.objects.create(name="Test OC",workgroup=self.wg)
        self.pr = models.Property.objects.create(name="Test P",workgroup=self.wg)
        self.dec = models.DataElementConcept.objects.create(name="Test DEC",
            objectClass=self.oc,
            property=self.pr,
            workgroup=self.wg,
            )

        self.assertEqual(self.oc.statuses.count(),0)
        self.assertEqual(self.pr.statuses.count(),0)
        self.assertEqual(self.dec.statuses.count(),0)

        state=models.STATES.candidate
        self.ra.register(self.dec,state,user)
        self.assertEqual(self.oc.statuses.count(),0)
        self.assertEqual(self.pr.statuses.count(),0)
        self.assertEqual(self.dec.statuses.count(),1)

        state=models.STATES.standard
        self.ra.register(self.dec,state,user,cascade=True)
        self.assertEqual(self.dec.statuses.count(),1)
        self.assertEqual(self.oc.statuses.count(),1)
        self.assertEqual(self.pr.statuses.count(),1)

        self.assertEqual(self.oc.statuses.all()[0].state,state)
        self.assertEqual(self.pr.statuses.all()[0].state,state)
        self.assertEqual(self.dec.statuses.all()[0].state,state)

    def test_DataElementCascade(self):
        user = User.objects.create_superuser('super','','user')
        self.ra = models.RegistrationAuthority.objects.create(name="Test RA")
        self.wg = models.Workgroup.objects.create(name="Setup WG")
        self.oc = models.ObjectClass.objects.create(name="Test OC",workgroup=self.wg)
        self.pr = models.Property.objects.create(name="Test P",workgroup=self.wg)
        self.vd = models.ValueDomain.objects.create(name="Test VD",
                workgroup=self.wg,
                format = "X" ,
                maximumLength = 3,
                dataType = models.DataType.objects.create(name="Test DT",workgroup=self.wg)
                )
        self.dec = models.DataElementConcept.objects.create(name="Test DEC",
            objectClass=self.oc,
            property=self.pr,
            workgroup=self.wg,
            )
        self.de = models.DataElement.objects.create(name="Test DE",
            dataElementConcept=self.dec,
            valueDomain=self.vd,
            workgroup=self.wg,
            )

        self.assertEqual(self.oc.statuses.count(),0)
        self.assertEqual(self.pr.statuses.count(),0)
        self.assertEqual(self.vd.statuses.count(),0)
        self.assertEqual(self.dec.statuses.count(),0)
        self.assertEqual(self.de.statuses.count(),0)

        state=models.STATES.candidate
        self.ra.register(self.de,state,user)
        self.assertEqual(self.oc.statuses.count(),0)
        self.assertEqual(self.pr.statuses.count(),0)
        self.assertEqual(self.vd.statuses.count(),0)
        self.assertEqual(self.dec.statuses.count(),0)
        self.assertEqual(self.de.statuses.count(),1)

        state=models.STATES.standard
        self.ra.register(self.de,state,user,cascade=True)
        self.assertEqual(self.de.statuses.count(),1)
        self.assertEqual(self.dec.statuses.count(),1)
        self.assertEqual(self.vd.statuses.count(),1)
        self.assertEqual(self.oc.statuses.count(),1)
        self.assertEqual(self.pr.statuses.count(),1)

        self.assertEqual(self.oc.statuses.all()[0].state,state)
        self.assertEqual(self.pr.statuses.all()[0].state,state)
        self.assertEqual(self.vd.statuses.all()[0].state,state)
        self.assertEqual(self.dec.statuses.all()[0].state,state)
        self.assertEqual(self.de.statuses.all()[0].state,state)
