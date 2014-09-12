from django.db.models import signals
import aristotle_mdr

signals.post_syncdb.connect(aristotle_mdr.models.defaultData(), sender=aristotle_mdr)