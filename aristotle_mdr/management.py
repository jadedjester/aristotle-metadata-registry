from django.db.models import signals
from django.contrib.auth.models import User
import aristotle_mdr
import sys
from django.conf import settings

def loadDefaultData(**kwargs): # pragma: no cover
    aristotle_mdr.models.defaultData()

def configureSystemUser(**kwargs):
    # Make a system "user" this is used for when the syetms needs post messages
    system = User.objects.create_user("aristotle")
    system.is_staff = False
    system.save()

signals.post_syncdb.connect(configureSystemUser, sender=aristotle_mdr.models)
signals.post_syncdb.connect(loadDefaultData, sender=aristotle_mdr.models)


# These are not used during testing.
def loadExampleData(**kwargs): # pragma: no cover
    print "Loading Aristotle-MDR test data because DEBUG is set to True."
    # Disable notification signals disabled as not everything will be setup yet.
    signals.post_save.disconnect(aristotle_mdr.models.concept_saved)
    aristotle_mdr.models.exampleData()
    signals.post_save.connect(aristotle_mdr.models.concept_saved)
if 'test' not in sys.argv and getattr(settings, 'DEBUG', "") == True:  # pragma: no cover
    signals.post_syncdb.connect(loadExampleData, sender=aristotle_mdr.models)