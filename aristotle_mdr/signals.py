from django.db.models.signals import post_save, post_delete
import haystack.signals as signals #.RealtimeSignalProcessor as RealtimeSignalProcessor
# Don't import aristotle_mdr.models directly, only pull in whats required,
#  otherwise Haystack gets into a circular dependancy.

class AristotleSignalProcessor(signals.RealtimeSignalProcessor):
    def setup(self):
        from aristotle_mdr.models import Status, _concept
        post_save.connect(self.handle_status_change, sender=Status)
        post_delete.connect(self.handle_status_change, sender=Status)
        post_save.connect(self.handle_concept_save, sender=_concept)
        post_delete.connect(self.handle_concept_delete, sender=Status)

        super(AristotleSignalProcessor,self).setup()

    def teardown(self): # pragma: no cover
        from aristotle_mdr.models import Status
        post_save.disconnect(self.handle_status_change, sender=Status)
        post_delete.disconnect(self.handle_status_change, sender=Status)
        super(AristotleSignalProcessor,self).teardown()

    def handle_status_change(self, sender, instance, **kwargs):
        # When a status changes, force an update of the object
        obj = instance.concept.item
        super(AristotleSignalProcessor,self).handle_save(obj.__class__,obj)

    def handle_concept_save(self, sender, instance, **kwargs):
        obj = instance.item
        self.handle_save(obj.__class__,obj)

    def handle_concept_delete(self, sender, instance, **kwargs):
        obj = instance.item
        self.handle_save(obj.__class__,obj)
