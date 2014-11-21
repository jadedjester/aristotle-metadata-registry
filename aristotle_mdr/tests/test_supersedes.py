from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
import aristotle_mdr.models as models
import aristotle_mdr.tests.utils as utils

from django.test.utils import setup_test_environment
setup_test_environment()

class SupersededProperty(TestCase):
    def setUp(self):
        self.wg = models.Workgroup.objects.create(name="Test WG")
        self.item1 = models.ObjectClass.objects.create(name="OC1",workgroup=self.wg)
        self.item2 = models.ObjectClass.objects.create(name="OC2",workgroup=self.wg)
        self.ra = models.RegistrationAuthority.objects.create(name="Test RA")

    def test_is_supersede_property(self):
        self.assertFalse(self.item1.is_superseded)
        self.item1.superseded_by = self.item2
        self.item1.save()
        self.assertTrue(self.item1.is_superseded)

        s = models.Status.objects.create(
                concept=self.item1,
                registrationAuthority=self.ra,
                registrationDate=timezone.now(),
                state=self.ra.public_state
                )
        #self.item1=models.ObjectClass.objects.get(id=self.item1.id)

        self.assertFalse(self.item1.is_superseded)
        s.state = models.STATES.superseded
        s.save()
        self.assertTrue(self.item1.is_superseded)


class SupersedePage(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(SupersedePage, self).setUp()

        # There would be too many tests to test every item type against every other
        # But they all have identical logic, so one test should suffice
        self.item1 = models.ObjectClass.objects.create(name="OC1",workgroup=self.wg1)
        self.item2 = models.ObjectClass.objects.create(name="OC2",workgroup=self.wg1)
        self.item3 = models.ObjectClass.objects.create(name="OC3",workgroup=self.wg2)
        self.item4 = models.Property.objects.create(name="Prop4",workgroup=self.wg1)

    def test_supersede(self):
        self.logout()
        response = self.client.get(reverse('aristotle:supersede',args=[self.item1.id]))
        self.assertRedirects(response,
            reverse("django.contrib.auth.views.login",)+"?next="+
            reverse('aristotle:supersede',args=[self.item1.id])
            )

        self.login_editor()
        response = self.client.get(reverse('aristotle:supersede',args=[self.item1.id]))
        self.assertEqual(response.status_code,200)
        self.assertEqual(self.item1.superseded_by,None)

        response = self.client.post(reverse('aristotle:supersede',args=[self.item1.id]),{'newerItem': self.item1.id})
        self.assertEqual(response.status_code,200) # An item cannot supersede itself, so it did not save and was served the form again.
        self.assertEqual(models.ObjectClass.objects.get(id=self.item1.id).superseded_by,None)

        response = self.client.post(reverse('aristotle:supersede',args=[self.item1.id]),{'newerItem': self.item2.id})
        self.assertEqual(response.status_code,302) # Item 2 can supersede item 1, so this saved and redirected properly.
        self.assertEqual(models.ObjectClass.objects.get(id=self.item1.id).superseded_by,self.item2)

        response = self.client.post(reverse('aristotle:supersede',args=[self.item1.id]),{'newerItem': self.item3.id})
        self.assertEqual(response.status_code,200) # Item 3 is a different workgroup, and the editor cannot see it , so cannot supersede, so it did not save and was served the form again.
        self.assertEqual(models.ObjectClass.objects.get(id=self.item1.id).superseded_by,self.item2)

        response = self.client.post(reverse('aristotle:supersede',args=[self.item1.id]),{'newerItem': self.item4.id})
        self.assertEqual(response.status_code,200) # Item 4 is a different type, so cannot supersede, so it did not save and was served the form again.
        self.assertEqual(models.ObjectClass.objects.get(id=self.item1.id).superseded_by,self.item2)

class DeprecatePage(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(DeprecatePage, self).setUp()

        # There would be too many tests to test every item type against every other
        # But they all have identical logic, so one test should suffice
        self.item1 = models.ObjectClass.objects.create(name="OC1",workgroup=self.wg1)
        self.item2 = models.ObjectClass.objects.create(name="OC2",workgroup=self.wg1)
        self.item3 = models.ObjectClass.objects.create(name="OC3",workgroup=self.wg1)
        self.item4 = models.Property.objects.create(name="VD3",workgroup=self.wg1)

        # There would be too many tests to test every item type against every other
        # But they all have identical logic, so one test should suffice
        self.item1 = models.ObjectClass.objects.create(name="OC1",workgroup=self.wg1)
        self.item2 = models.ObjectClass.objects.create(name="OC2",workgroup=self.wg1)
        self.item3 = models.ObjectClass.objects.create(name="OC3",workgroup=self.wg2)
        self.item4 = models.Property.objects.create(name="Prop4",workgroup=self.wg1)

    def test_deprecate(self):
        self.logout()
        response = self.client.get(reverse('aristotle:deprecate',args=[self.item1.id]))
        self.assertRedirects(response,
            reverse("django.contrib.auth.views.login",)+"?next="+
            reverse('aristotle:deprecate',args=[self.item1.id])
            )

        self.login_editor()
        response = self.client.get(reverse('aristotle:deprecate',args=[self.item1.id]))
        self.assertEqual(response.status_code,200)
        self.assertListEqual(list(self.item1.supersedes.all()),[])

        response = self.client.post(reverse('aristotle:deprecate',args=[self.item1.id,]),{'olderItems': [self.item1.id,]})
        self.assertEqual(response.status_code,200) # An item cannot deprecate itself, so it did not save and was served the form again.
        self.assertListEqual(list(self.item1.supersedes.all()),[])

        response = self.client.post(reverse('aristotle:deprecate',args=[self.item1.id,]),{'olderItems': [self.item2.id,self.item3.id]})
        self.assertEqual(response.status_code,200) #  Item 3 is a different workgroup, and the editor cannot see it , so cannot deprecate, so it did not save and was served the form again.
        self.assertListEqual(list(self.item1.supersedes.all()),[])

        response = self.client.post(reverse('aristotle:deprecate',args=[self.item1.id,]),{'olderItems': [self.item2.id,]})
        self.assertEqual(response.status_code,302) # Item 2 can deprecate item 1, so this saved and redirected properly.
        self.assertListEqual(list(self.item1.supersedes.all()),[self.item2])

        response = self.client.post(reverse('aristotle:deprecate',args=[self.item1.id,]),{'olderItems': [self.item3.id,]})
        self.assertEqual(response.status_code,200) # Item 3 is a different workgroup, and the editor cannot see it , so cannot deprecate, so it did not save and was served the form again.
        self.assertListEqual(list(self.item1.supersedes.all()),[self.item2])

        response = self.client.post(reverse('aristotle:deprecate',args=[self.item1.id]),{'olderItems': [self.item4.id]})
        self.assertEqual(response.status_code,200) # Item 4 is a different type, so cannot deprecate, so it did not save and was served the form again.
        self.assertListEqual(list(self.item1.supersedes.all()),[self.item2])

