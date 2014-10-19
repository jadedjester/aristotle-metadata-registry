from django.test import TestCase, Client
from aristotle_mdr import models, perms
from django.utils import timezone
from django.core.urlresolvers import reverse
from aristotle_mdr.tests import utils

from django.test.utils import setup_test_environment
setup_test_environment()

class AdminPage(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(AdminPage, self).setUp()

    def test_editor_make_item(self):
        self.login_editor()
        response = self.client.get(reverse("admin:aristotle_mdr_objectclass_changelist"))
        self.assertEqual(response.status_code,200)
        response = self.client.get(reverse("admin:aristotle_mdr_objectclass_add"))
        self.assertEqual(response.status_code,200)
        # make an item
        response = self.client.post(reverse("admin:aristotle_mdr_objectclass_add"),
                    {'name':"admin_page_test_oc",'description':"test","workgroup":self.wg1.id}
                )
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("admin:aristotle_mdr_objectclass_changelist"))
        self.assertEqual(self.wg1.items.first().name,"admin_page_test_oc")
        self.assertEqual(self.wg1.items.count(),1)

        # Editor can't save in WG2, so this won't redirect.
        response = self.client.post(reverse("admin:aristotle_mdr_objectclass_add"),
                    {'name':"admin_page_test_oc",'description':"test","workgroup":self.wg2.id}
                )
        self.assertEqual(self.wg2.items.count(),0)
        self.assertEqual(response.status_code,200)
"""
    def test_editor_deleting(self):
        self.login_editor()
        # make an item
        response = self.client.post(reverse("admin:aristotle_mdr_objectclass_add"),
                    {'name':"admin_page_test_oc",'description':"test","workgroup":self.wg1.id}
                )
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("admin:aristotle_mdr_objectclass_changelist"))
        self.assertEqual(self.wg1.items.count(),1)
        print "here"
        response = self.client.get(reverse("admin:aristotle_mdr_objectclass_delete",args=(str(self.wg1.items.first().id))))
        print response.context
        self.assertEqual(self.wg1.items.count(),0)
        print "here"

        response = self.client.post(reverse("admin:aristotle_mdr_objectclass_add"),
                    {'name':"admin_page_test_oc",'description':"test","workgroup":self.wg1.id}
                )
        self.assertEqual(self.wg1.items.count(),1)
        self.ra.register(self.wg1.items.first(),models.STATES.standard,self.registrar)
        self.assertTrue(self.wg1.items.first().is_registered)

        response = self.client.get(reverse("admin:aristotle_mdr_objectclass_delete",args=(self.wg1.items.first().id)))
        print response.context
        self.assertEqual(self.wg1.items.count(),1)
"""