from django.test import TestCase, Client
from aristotle_mdr import models, perms
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django.test.utils import setup_test_environment
setup_test_environment()

from aristotle_mdr.tests import utils

class TestSearch(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(TestSearch, self).setUp()

        self.ra = models.RegistrationAuthority.objects.create(name="Kelly Act")
        self.registrar = User.objects.create_user('stryker','william.styker@senate.gov','mutantsMustDie')
        self.ra.giveRoleToUser('Registrar',self.registrar)
        xmen = "wolverine cyclops professorX storm nightcrawler"
        self.xmen_wg = models.Workgroup.objects.create(name="X Men")

        self.item_xmen = [
            models.ObjectClass.objects.create(name=t,description="known x-man",workgroup=self.xmen_wg)\
            for t in xmen.split() ]
        for item in self.item_xmen:
            self.ra.register(item,models.STATES.standard,self.registrar)

        avengers = "thor spiderman ironman hulk captainAmerica"

        self.avengers_wg = models.Workgroup.objects.create(name="Avengers")
        self.item_avengers = [
            models.ObjectClass.objects.create(name=t,workgroup=self.avengers_wg)
            for t in avengers.split() ]

        self.item1 = models.ObjectClass.objects.create(name="OC1",workgroup=self.wg1)
        self.item2 = models.ObjectClass.objects.create(name="OC2",workgroup=self.wg1)
        self.ra = models.RegistrationAuthority.objects.create(name="Test RA")

    def test_public_search(self):
        self.logout()
        response = self.client.get(reverse('aristotle:search')+"?q=xman")
        self.assertEqual(response.status_code,200)
        for i in response.context['page'].object_list:
            self.assertTrue(i.object.is_public())
