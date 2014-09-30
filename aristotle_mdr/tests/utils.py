from aristotle_mdr import models, perms
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class LoggedInViewPages(object):
    """
    This helps us manage testing across different user types.
    """
    def setUp(self):

        self.client = Client()
        self.wg1 = models.Workgroup.objects.create(name="Test WG 1") # Editor is member
        self.wg2 = models.Workgroup.objects.create(name="Test WG 2")
        self.ra = models.RegistrationAuthority.objects.create(name="Test RA")

        self.su = User.objects.create_superuser('super','','user')
        self.manager = User.objects.create_user('mandy','','manager')
        self.editor = User.objects.create_user('eddie','','editor')
        self.viewer = User.objects.create_user('vicky','','viewer')
        self.registrar = User.objects.create_user('reggie','','registrar')

        self.wg1.addUser(self.editor)
        self.wg1.giveRoleToUser('Editor',self.editor)
        self.wg1.addUser(self.editor)
        self.wg1.giveRoleToUser('Manager',self.manager)
        self.wg1.addUser(self.viewer)
        self.wg1.giveRoleToUser('Viewer',self.viewer)
        self.ra.giveRoleToUser('Registrar',self.registrar)

        self.editor = User.objects.get(pk=self.editor.pk)
        self.manager = User.objects.get(pk=self.manager.pk)
        self.viewer = User.objects.get(pk=self.viewer.pk)
        self.registrar = User.objects.get(pk=self.registrar.pk)

    def get_page(self,item):
        return reverse('aristotle:%s'%self.url_name,args=[item.id])

    def logout(self):
        self.client.post(reverse('django.contrib.auth.views.logout'), {})

    def login_superuser(self):
        self.logout()
        response = self.client.post(reverse('django.contrib.auth.views.login'), {'username': 'super', 'password': 'user'})
        self.assertEqual(response.status_code,302)
        return response
    def login_viewer(self):
        self.logout()
        response = self.client.post(reverse('django.contrib.auth.views.login'), {'username': 'vicky', 'password': 'viewer'})
        self.assertEqual(response.status_code,302)
        return response
    def login_registrar(self):
        self.logout()
        response = self.client.post(reverse('django.contrib.auth.views.login'), {'username': 'reggie', 'password': 'registrar'})
        self.assertEqual(response.status_code,302)
        return response
    def login_editor(self):
        self.logout()
        response = self.client.post(reverse('django.contrib.auth.views.login'), {'username': 'eddie', 'password': 'editor'})
        self.assertEqual(response.status_code,302)
        return response
    def login_manager(self):
        self.logout()
        response = self.client.post(reverse('django.contrib.auth.views.login'), {'username': 'mandy', 'password': 'manager'})
        self.assertEqual(response.status_code,302)
        return response

    def test_logins(self):
        # Failed logins reutrn 200, not 401
        # See http://stackoverflow.com/questions/25839434/
        response = self.client.post(reverse('django.contrib.auth.views.login'), {'username': 'super', 'password': 'the_wrong_password'})
        self.assertEqual(response.status_code,200)
        # Success redirects to the homepage, so its 302 not 200
        response = self.client.post(reverse('django.contrib.auth.views.login'), {'username': 'super', 'password': 'user'})
        self.assertEqual(response.status_code,302)
        self.logout()
        response = self.client.post(reverse('django.contrib.auth.views.login'), {'username': 'eddie', 'password': 'editor'})
        self.assertEqual(response.status_code,302)
        self.logout()
        response = self.client.post(reverse('django.contrib.auth.views.login'), {'username': 'vicky', 'password': 'viewer'})
        self.assertEqual(response.status_code,302)
        self.logout()
        response = self.client.post(reverse('django.contrib.auth.views.login'), {'username': 'reggie', 'password': 'registrar'})
        self.assertEqual(response.status_code,302)
        self.logout()
