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
