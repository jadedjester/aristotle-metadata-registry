from notifications import notify
#from aristotle_mdr.models import _concept
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

def favourite_updated(recipient,obj):
    notify.send(recipient, recipient=recipient, verb="changed a favourited item", target=obj)

def workgroup_item_updated(recipient,obj):
    notify.send(recipient, recipient=recipient, verb="changed a item in the workgroup", target=obj)
def workgroup_item_new(recipient,obj):
    notify.send(recipient, recipient=recipient, verb="a new item in the workgroup", target=obj)

@receiver(post_save, sender='aristotle_mdr.models._concept')
def concept_saved(sender, instance, created, **kwargs):
    print "I GOT THIS ------------------------------------------------------------------"
    for p in instance.favourited_by.all():
        favourite_updated(recipient=p.user,obj=instance)
    for p in instance.workgroup.viewers():
        if created:
            workgroup_item_new(recipient=p.user,obj=instance)
        else:
            workgroup_item_updated(recipient=p.user,obj=instance)