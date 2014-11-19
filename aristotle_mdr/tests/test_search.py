from django.test import TestCase

import aristotle_mdr.models as models
import aristotle_mdr.tests.utils as utils
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django.test.utils import setup_test_environment
setup_test_environment()

class TestSearch(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(TestSearch, self).setUp()

        self.ra = models.RegistrationAuthority.objects.create(name="Kelly Act")
        self.registrar = User.objects.create_user('stryker','william.styker@weaponx.mil','mutantsMustDie')
        self.ra.giveRoleToUser('Registrar',self.registrar)
        xmen = "professorX cyclops iceman angel beast phoenix wolverine storm nightcrawler"
        self.xmen_wg = models.Workgroup.objects.create(name="X Men")
        self.xmen_wg.registrationAuthorities.add(self.ra)
        self.xmen_wg.save()

        self.item_xmen = [
            models.ObjectClass.objects.create(name=t,description="known x-man",workgroup=self.xmen_wg,readyToReview=True)\
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

class TestTokenSearch(TestCase):
    def setUp(self):
        from django.test import Client

        self.client = Client()
        self.ra = models.RegistrationAuthority.objects.create(name="Kelly Act")
        self.registrar = User.objects.create_user('stryker','william.styker@weaponx.mil','mutantsMustDie')
        self.ra.giveRoleToUser('registrar',self.registrar)
        xmen = "professorX cyclops iceman angel beast phoenix wolverine storm nightcrawler"
        self.xmen_wg = models.Workgroup.objects.create(name="X Men")
        self.xmen_wg.registrationAuthorities.add(self.ra)
        self.xmen_wg.save()

        self.item_xmen = [
            models.ObjectClass.objects.create(name=t,version="0.%d.0"%(v+1),description="known x-man",workgroup=self.xmen_wg,readyToReview=True)
            for v,t in enumerate(xmen.split()) ]
        for item in self.item_xmen:
            self.ra.register(item,models.STATES.standard,self.registrar)
    def test_token_search(self):

        response = self.client.get(reverse('aristotle:search')+"?q=version:0.1.0")
        self.assertEqual(response.status_code,200)
        objs = response.context['page'].object_list
        self.assertEqual(len(objs),1)
        self.assertTrue(objs[0].object.name,"wolverine")
