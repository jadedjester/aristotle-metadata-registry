class MyAdaptorEditInline(object):

    @classmethod
    def can_edit(cls, adaptor_field):
        user = adaptor_field.request.user
        obj = adaptor_field.obj
        return user_can_edit(user,obj)

def user_can_alter_comment(user,comment):
    return user.is_superuser or user == comment.author or user_is_workgroup_manager(user,comment.post.workgroup)
def user_can_alter_post(user,post):
    return user.is_superuser or user == post.author or user_is_workgroup_manager(user,post.workgroup)


def user_can_view(user,item):
    """Can the user view the item?"""

    #if user is None: return item.is_public()
    if user.is_superuser:
        return True
    # A user can view their own details
    if hasattr(item, "profile"):
        return item == user

    return item.can_view(user)

def user_is_editor(user,workgroup=None):
    if user.is_superuser:
        return True
    elif workgroup is None:
        return user.submitter_in.count() > 0 or user.steward_in.count() > 0
    else:
        return user.submitter_in.filter(workgroup=workgroup).exists() or \
                user.steward_in.filter(workgroup=workgroup).exists()

def user_is_registrar(user,ra=None):
    if user.is_superuser:
        return True
    elif ra is None:
        return user.registrar_in.count() > 0
    else:
        return user in ra.registrars.all()


def user_is_workgroup_manager(user,workgroup=None):
    if user.is_superuser:
        return True
    elif workgroup is None:
        return user.workgroup_manager_in.count() > 0
    else:
        return user in workgroup.managers.all()

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
        return user.registrar_in.count() > 0 and \
                True in (user in ra.registrars.all()
                        for ra in item.workgroup.registrationAuthorities.all())
    return False

def user_can_edit(user,item):
    """Can the user edit the item?"""

    #non-logged in users can't edit anything
    if user.is_anonymous():
        return False
    if not user_can_view(user,item):
        return False
    if user.is_superuser:
        return True
    # A user can edit their own details
    if hasattr(item, "profile"):
        return item == user
    return item.can_edit(user)


def user_in_workgroup(user,wg):
    if user.is_superuser:
        return True
    return user in wg.members


