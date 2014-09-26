from django.contrib.auth.models import User

class MyAdaptorEditInline(object):

    @classmethod
    def can_edit(cls, adaptor_field):
        user = adaptor_field.request.user
        obj = adaptor_field.obj
        return user_can_edit(user,obj)

def user_can_alter_comment(user,comment):
    return user == comment.author or user_is_workgroup_manager(user,comment.post.workgroup)
def user_can_alter_post(user,post):
    return user == post.author or user_is_workgroup_manager(user,post.workgroup)


def user_can_view(user,item):
    """Can the user view the item?"""

    #if user is None: return item.is_public()
    if user.is_superuser:
        return True
    # A user can view their own details
    if hasattr(item, "profile"):
        return item == user
    if item.is_managed:
        # If the above works, we have a managed Item
        if item.is_public():
            return True
        else:
            if user.is_anonymous():
                return False
        # If the user can view objects in this workgroup
        if user.has_perm('aristotle_mdr.view_in_{wg}'.format(wg=item.workgroup.name)):
            return True
        # if the item is registered and the user is a registrar view view permissions in that authority.
        if item.is_registered:
            for s in item.statuses.all():
                ra = s.registrationAuthority
                if user.has_perm('aristotle_mdr.view_registered_in_{name}'.format(name=ra.name)):
                    return True
        return False
    else:
        return True

def user_is_registrar(user):
    if user.is_superuser:
        return True
    return True in (user.has_perm('aristotle_mdr.promote_in_{name}'.format(name=r.name))
            for r in user.profile.registrationAuthorities.all()
         )

def user_is_registrar_in_ra(user,ra):
    if user.is_superuser:
        return True
    return user.has_perm('aristotle_mdr.promote_in_{name}'.format(name=ra.name))

def user_is_workgroup_manager(user,workgroup):
    if user.is_superuser:
        return True
    return user.has_perm('aristotle_mdr.admin_in_{name}'.format(name=workgroup.name))

def user_can_change_status(user,item):
    """Can the user change the status of the item?"""

    # Cache if the user can view as we use it a few times.
    can_view = user_can_view(user,item)
    if not can_view:
        return False
    if user.is_superuser:
        return True
    # TODO: restrict to only those registration authorities of that items based on the items workgroup, unless the item is visible to the user.
    if can_view or item.readyToReview:
        return True in (user.has_perm('aristotle_mdr.promote_in_{name}'.format(name=r.name))
                for r in user.profile.registrationAuthorities.all()
             )
    return False

def user_can_edit(user,item):
    """Can the user edit the item?"""

    #non-logged in users can't edit anything
    if not user.is_active:
        return False
    if not user_can_view(user,item):
        return False
        #raise PermissionDenied()
    if user.is_superuser:
        return True
    # A user can edit their own details
    if hasattr(item, "profile"):
        return item == user
    elif item.is_managed:
        if item.is_locked():
            return user.has_perm('aristotle_mdr.edit_locked_in_{wg}'.format(wg=item.workgroup.name))
        else:
            return user.has_perm('aristotle_mdr.edit_unlocked_in_{wg}'.format(wg=item.workgroup.name))
    elif item.is_workgroup:
        return user_is_workgroup_manager(user,item)
    return False

def user_in_workgroup(user,wg):
    if user.is_superuser:
        return True
    return wg in user.profile.workgroups.all()


