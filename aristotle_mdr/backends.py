from django.contrib.auth.backends import ModelBackend
from django.conf import settings

class AristotleBackend(ModelBackend):
    def has_module_perms(self, user_obj, app_label):
        """
        Returns True if the requested app is an extension.
        Actual permissions to edit/change content is covered in aristotle_mdr.admin
        Otherwise, it returns as per Django
        """
        extensions = getattr(settings, 'ARISTOTLE_SETTINGS', {}).get('CONTENT_EXTENSIONS',[])
        if app_label in extensions:
            return True
        return super(AristotleBackend, self).has_module_perms(user_obj, app_label)
