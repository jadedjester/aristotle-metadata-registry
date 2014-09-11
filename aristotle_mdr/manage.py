from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.utils.translation import ugettext as _
from django import forms

import aristotle_mdr.models as MDR
import aristotle_mdr.admin as baseAdmin

from django.contrib.auth.forms import AuthenticationForm

class UserAdminAuthenticationForm(AuthenticationForm):
    """
    Same as Django's AdminAuthenticationForm but allows to login
    any user who is not staff.
    """
    this_is_the_login_form = forms.BooleanField(widget=forms.HiddenInput,
                                initial=1,
                                error_messages={'required': _(
                                "Please log in again, because your session has"
                                " expired.")})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE

        if username and password:
            self.user_cache = authenticate(username=username,
            password=password)
            if self.user_cache is None:
                if u'@' in username:
                    # Mistakenly entered e-mail address instead of username?
                    # Look it up.
                    try:
                        user = MDR.User.objects.get(email=username)
                    except (MDR.User.DoesNotExist, MDR.User.MultipleObjectsReturned):
                        # Nothing to do here, moving along.
                        pass
                    else:
                        if user.check_password(password):
                            message = _("Your e-mail address is not your "
                                        "username."
                                        " Try '%s' instead.") % user.username
                raise forms.ValidationError(message)
            # Removed check for is_staff here!
            elif not self.user_cache.is_active:
                raise forms.ValidationError(message)
        self.check_for_test_cookie()
        return self.cleaned_data

class UserAdmin(AdminSite):

    login_form = UserAdminAuthenticationForm

    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active

user_admin_site = UserAdmin(name='usersadmin')
# Run user_admin_site.register() for each model we wish to register
# for our admin interface for users

user_admin_site.register(MDR.DataElement,baseAdmin.DataElementAdmin)
user_admin_site.register(MDR.DataElementConcept,baseAdmin.DataElementConceptAdmin)
user_admin_site.register(MDR.ValueDomain,baseAdmin.ValueDomainAdmin)
user_admin_site.register(MDR.Property)
user_admin_site.register(MDR.ObjectClass,baseAdmin.ObjectClassAdmin)
user_admin_site.register(MDR.Workgroup,baseAdmin.WorkgroupAdmin)
user_admin_site.register(baseAdmin.CodeList,baseAdmin.CodeListAdmin)


ERROR_MESSAGE = "Like a balloon when something bad happens"

