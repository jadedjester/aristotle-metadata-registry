from django.contrib.auth.backends import ModelBackend
from django.conf import settings

from aristotle_mdr import perms

class AristotleBackend(ModelBackend):
    def has_module_perms(self, user_obj, app_label):
        """
        Returns True if the requested app is an extension.
        Actual permissions to edit/change content are covered in aristotle_mdr.admin
        Otherwise, it returns as per Django permissions
        """
        if not user_obj.is_active:
            return False
        extensions = getattr(settings, 'ARISTOTLE_SETTINGS', {}).get('CONTENT_EXTENSIONS',[])
        if app_label in extensions:
            return perms.user_is_editor(user_obj)
        return super(AristotleBackend, self).has_module_perms(user_obj, app_label)

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active:
            return False
        app_label,perm_name = perm.split('.',1)
        extensions = getattr(settings, 'ARISTOTLE_SETTINGS', {}).get('CONTENT_EXTENSIONS',[])

        if app_label in extensions or app_label == "aristotle_mdr":
            # This is a rough catch all, and is designed to indicate a user could delete an item type
            # But not a specific item.
            if perm_name.startswith('delete_'):
                if obj is None and perm is not "aristotle_mdr.delete_concept_from_admin":
                    return perms.user_is_editor(user_obj)

        if perm.startswith("aristotle_mdr.delete_"):
            if obj is None and perm is not "aristotle_mdr.delete_concept_from_admin":
                # This is a rough catch all, and will fail for extension items.
                return perms.user_is_editor(user_obj)
            if perm == "aristotle_mdr.delete_concept_from_admin":
                return obj is None or perms.user_can_edit(user_obj,obj)
        return super(AristotleBackend, self).has_perm(user_obj, perm, obj)
