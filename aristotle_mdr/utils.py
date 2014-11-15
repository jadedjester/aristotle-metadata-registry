from django.forms import model_to_dict

def concept_to_dict(obj):
    """
    A replacement for the ```django.form.model_to_dict`` that includes additional
    ``ManyToManyFields``, but removes certain concept fields.
    """

    excluded_fields='readyToReview version workgroup pk id supersedes superseded_by'.split()
    concept_dict = model_to_dict(obj,
        fields=[field.name for field in obj._meta.fields if field.name not in excluded_fields],
        exclude=excluded_fields
        )
    return concept_dict

def concept_to_clone_dict(obj):
    """
    An extension of ``aristotle_mdr.utils.concept_to_dict`` that adds a 'clone'
    suffix to the name when cloning an item.
    """

    from django.utils.translation import ugettext # Do at run time because reasons
    clone_dict = concept_to_dict(obj)
    clone_dict['name'] = clone_dict['name'] + ugettext(u" (clone)")
    return clone_dict

'''
Modified from: https://djangosnippets.org/snippets/2524/
'''
from django.core.cache import cache
# "There are only two hard problems in Computer Science: cache invalidation, naming things and off-by-one errors"
def cache_per_item_user(ttl=None, prefix=None, cache_post=False):
    def decorator(function):
        def apply_cache(request, *args, **kwargs):
            # Gera a parte do usuario que ficara na chave do cache
            if request.user.is_anonymous():
                user = 'anonymous'
            else:
                user = request.user.id

            iid = kwargs['iid']

            if prefix:
                CACHE_KEY = '%s_%s_%s'%(prefix, user, iid)
            else:
                CACHE_KEY = 'view_cache_%s_%s_%s'%(function.__name__, user, iid)

            if not cache_post and request.method == 'POST':
                can_cache = False
            else:
                can_cache = True

            from aristotle_mdr.models import _concept
            import datetime
            from django.utils import timezone

            if 'nocache' not in request.GET.keys():
                can_cache = False

            # If the item was modified in the last 15 seconds, don't use cache
            recently = timezone.now() - datetime.timedelta(seconds=15)
            if _concept.objects.filter(id=iid,modified__gte=recently).exists():
                can_cache = False

            if can_cache:
                response = cache.get(CACHE_KEY, None)
            else:
                response = None

            if not response:
                response = function(request, *args, **kwargs)
                if can_cache:
                    cache.set(CACHE_KEY, response, ttl)
            return response
        return apply_cache
    return decorator
