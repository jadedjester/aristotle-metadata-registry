from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("favourite_updated", _("Favourited item updated"), _("An item you favourited has been edited"))
        notification.create_notice_type("worgroup_updated", _("Workgroup item updated"), _("An item in one of your workgroups has been edited"))

    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"
