from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import setup_test_environment

import aristotle_mdr.models as models
import aristotle_mdr.tests.utils as utils

setup_test_environment()

class AdminPage(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(AdminPage, self).setUp()

    def test_clone(self):
        from aristotle_mdr.utils import concept_to_clone_dict

        # Does cloning an item prepopulate everythin?
        self.login_editor()
        oc = models.ObjectClass.objects.create(name="OC1",workgroup=self.wg1)
        prop = models.Property.objects.create(name="Prop1",workgroup=self.wg1)
        dec = models.DataElementConcept.objects.create(name="DEC1",objectClass=oc,property=prop,workgroup=self.wg1)

        response = self.client.get(reverse("admin:aristotle_mdr_dataelementconcept_add")+"?clone=%s"%dec.id)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['adminform'].form.initial,concept_to_clone_dict(dec))

    def test_name_suggests(self):
        self.login_editor()
        oc = models.ObjectClass.objects.create(name="OC1",workgroup=self.wg1)
        prop = models.Property.objects.create(name="Prop1",workgroup=self.wg1)
        dec = models.DataElementConcept.objects.create(name="DEC1",objectClass=oc,property=prop,workgroup=self.wg1)

        response = self.client.get(reverse("admin:aristotle_mdr_dataelementconcept_change",args=(str(dec.id))))
        self.assertEqual(response.status_code,200)

    def test_su_can_add_new_user(self):
        self.login_superuser()
        response = self.client.post(reverse("admin:auth_user_add"),
            {'username':"newuser",'password1':"test",'password2':"test",
                'profile-TOTAL_FORMS': 1, 'profile-INITIAL_FORMS': 0, 'profile-MAX_NUM_FORMS': 1,
                'profile-0-workgroup_manager_in': [self.wg1.id],
                'profile-0-steward_in': [self.wg1.id],
                'profile-0-submitter_in': [self.wg1.id],
                'profile-0-viewer_in': [self.wg1.id],
                'profile-0-registrationauthority_manager_in': [self.ra.id],
                'profile-0-registrar_in': [self.ra.id],

            }
        )
        self.assertEqual(response.status_code,302)
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.profile.workgroups.count(),1)
        self.assertEqual(new_user.profile.workgroups.first(),self.wg1)
        self.assertEqual(new_user.profile.registrarAuthorities.count(),1)
        self.assertEqual(new_user.profile.registrarAuthorities.first(),self.ra)
        for rel in [new_user.workgroup_manager_in,
                    new_user.steward_in,
                    new_user.submitter_in,
                    new_user.viewer_in]:
            self.assertEqual(rel.count(),1)
            self.assertEqual(rel.first(),self.wg1)
        for rel in [new_user.registrationauthority_manager_in,
                    new_user.registrar_in,]:
            self.assertEqual(rel.count(),1)
            self.assertEqual(rel.first(),self.ra)

        response = self.client.post(reverse("admin:auth_user_add"),
            {'username':"newuser_with_none",'password1':"test",'password2':"test",
                'profile-TOTAL_FORMS': 1, 'profile-INITIAL_FORMS': 0, 'profile-MAX_NUM_FORMS': 1,
            }
        )
        self.assertEqual(response.status_code,302)
        new_user = User.objects.get(username='newuser_with_none')
        self.assertEqual(new_user.profile.workgroups.count(),0)
        self.assertEqual(new_user.profile.registrarAuthorities.count(),0)
        for rel in [new_user.workgroup_manager_in,
                    new_user.steward_in,
                    new_user.submitter_in,
                    new_user.viewer_in]:
            self.assertEqual(rel.count(),0)
        for rel in [new_user.registrationauthority_manager_in,
                    new_user.registrar_in,]:
            self.assertEqual(rel.count(),0)


    def test_supersede_saves(self):
        pass

    def test_editor_change_item(self):
        pass

    def test_editor_make_item(self):
        self.login_editor()
        response = self.client.get(reverse("admin:aristotle_mdr_objectclass_changelist"))
        self.assertEqual(response.status_code,200)
        response = self.client.get(reverse("admin:aristotle_mdr_objectclass_add"))
        self.assertEqual(response.status_code,200)
        # make an item
        response = self.client.get(reverse("admin:aristotle_mdr_objectclass_add"))

        response = self.client.post(reverse("admin:aristotle_mdr_objectclass_add"),
                    {'name':"admin_page_test_oc",'description':"test","workgroup":self.wg1.id,
                        'statuses-TOTAL_FORMS': 0, 'statuses-INITIAL_FORMS': 0 #no substatuses
                    }
                )
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("admin:aristotle_mdr_objectclass_changelist"))
        self.assertEqual(self.wg1.items.first().name,"admin_page_test_oc")
        self.assertEqual(self.wg1.items.count(),1)

        # Editor can't save in WG2, so this won't redirect.
        response = self.client.post(reverse("admin:aristotle_mdr_objectclass_add"),
                    {'name':"admin_page_test_oc",'description':"test","workgroup":self.wg2.id,
                        'statuses-TOTAL_FORMS': 0, 'statuses-INITIAL_FORMS': 0 #no substatuses
                    }
                )
        self.assertEqual(self.wg2.items.count(),0)
        self.assertEqual(response.status_code,200)

    def test_editor_deleting(self):
        self.login_editor()
        # make some items
        self.item1 = models.ObjectClass.objects.create(name="OC1",workgroup=self.wg1)
        self.item2 = models.ObjectClass.objects.create(name="OC2",workgroup=self.wg2)

        self.assertEqual(self.wg1.items.count(),1)
        response = self.client.get(reverse("admin:aristotle_mdr_objectclass_delete",args=(str(self.item1.id))))
        self.assertEqual(response.status_code,200)
        response = self.client.post(
            reverse("admin:aristotle_mdr_objectclass_delete",args=(str(self.item1.id))),
            {'post':'yes'}
            )
        self.assertRedirects(response,reverse("admin:aristotle_mdr_objectclass_changelist"))
        self.assertEqual(self.wg1.items.count(),0)

        self.item1 = models.ObjectClass.objects.create(name="OC1",workgroup=self.wg1,readyToReview=True)
        self.assertEqual(self.wg1.items.count(),1)
        self.ra.register(self.item1,models.STATES.standard,self.registrar)
        self.assertTrue(self.item1.is_registered)

        response = self.client.get(reverse("admin:aristotle_mdr_objectclass_delete",args=(str(self.item1.id))))
        self.assertEqual(response.status_code,404)
        self.assertEqual(self.wg1.items.count(),1)
        response = self.client.post(
            reverse("admin:aristotle_mdr_objectclass_delete",args=(str(self.item1.id))),
            {'post':'yes'}
            )
        self.assertEqual(response.status_code,404)
        self.assertEqual(self.wg1.items.count(),1)

        response = self.client.get(reverse("admin:aristotle_mdr_objectclass_delete",args=(str(self.item2.id))))
        self.assertEqual(response.status_code,404)
        self.assertEqual(self.wg2.items.count(),1)
        response = self.client.post(
            reverse("admin:aristotle_mdr_objectclass_delete",args=(str(self.item2.id))),
            {'post':'yes'}
            )
        self.assertEqual(response.status_code,404)
        self.assertEqual(self.wg2.items.count(),1)
