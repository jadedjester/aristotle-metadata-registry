from django.db.models.signals import post_save, post_delete


from haystack.signals import RealtimeSignalProcessor
# Don't import aristotle_mdr.models directly, only pull in whats required,
#  otherwise Haystack gets into a circular dependancy.
from aristotle_mdr.models import Status

class AristotleSignalProcessor(RealtimeSignalProcessor):
    def setup(self):
        post_save.connect(self.handle_status_change, sender=Status)
        post_delete.connect(self.handle_status_change, sender=Status)
        super(AristotleSignalProcessor,self).setup()

    def teardown(self):
        post_save.disconnect(self.handle_status_change, sender=Status)
        post_delete.disconnect(self.handle_status_change, sender=Status)
        super(AristotleSignalProcessor,self).teardown()

    def handle_status_change(self, sender, instance, **kwargs):
        # When a status changes, force an update of the object
        obj = instance.concept.item
        super(AristotleSignalProcessor,self).handle_save(obj.__class__,obj)


