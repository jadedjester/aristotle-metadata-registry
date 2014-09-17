from django.db.models import signals
import aristotle_mdr
import sys

def loadDefaultData(**kwargs):
    aristotle_mdr.models.defaultData()

if 'test' not in sys.argv:
    signals.post_syncdb.connect(loadDefaultData, sender=aristotle_mdr)
