from django.db.models import signals
import aristotle_mdr
import sys

if 'test' not in sys.argv:
    signals.post_syncdb.connect(aristotle_mdr.models.defaultData(), sender=aristotle_mdr)