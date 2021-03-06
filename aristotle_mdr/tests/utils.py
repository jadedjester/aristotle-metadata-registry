import aristotle_mdr.models as models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class LoggedInViewPages(object):
    """
    This helps us manage testing across different user types.
    """
    def setUp(self):
        from django.test import Client

        self.client = Client()
        self.wg1 = models.Workgroup.objects.create(name="Test WG 1") # Editor is member
        self.wg2 = models.Workgroup.objects.create(name="Test WG 2")
        self.ra = models.RegistrationAuthority.objects.create(name="Test RA")
        self.wg1.registrationAuthorities.add(self.ra)
        self.wg1.save()

        self.su = User.objects.create_superuser('super','','user')
        self.manager = User.objects.create_user('mandy','','manager')
        self.manager.is_staff=True
        self.manager.save()
        self.editor = User.objects.create_user('eddie','','editor')
        self.editor.is_staff=True
        self.editor.save()
        self.viewer = User.objects.create_user('vicky','','viewer')
        self.registrar = User.objects.create_user('reggie','','registrar')

        self.wg1.submitters.add(self.editor)
        self.wg1.managers.add(self.manager)
        self.wg1.viewers.add(self.viewer)
        self.ra.registrars.add(self.registrar)

        self.editor = User.objects.get(pk=self.editor.pk)
        self.manager = User.objects.get(pk=self.manager.pk)
        self.viewer = User.objects.get(pk=self.viewer.pk)
        self.registrar = User.objects.get(pk=self.registrar.pk)

    def get_page(self,item):
        return reverse('aristotle:%s'%self.item1.url_name,args=[item.id])

    def get_help_page(self):
        return reverse('aristotle:%s'%self.item1.url_name)

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
