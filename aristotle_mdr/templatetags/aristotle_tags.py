#-*- coding: utf-8 -*-
"""
Tags and filters available in aristotle templates
=================================================

A number of convenience tags are available for performing common actions in custom
templates.

To use these make use you include the aristotle template tags ain every template that uses them, like so::

    {% load aristotle_tags %}

Available tags and filters
--------------------------
"""
from django import template
from aristotle_mdr import perms
from aristotle_mdr import models as MDR
from django.core.urlresolvers import reverse, resolve

register = template.Library()

@register.filter
def can_view(item,user):
    """
    A filter that acts as a wrapper around ``aristotle_mdr.perms.user_can_edit``.
    Returns true if the user has permission to view the item, otherwise it returns False.
    If calling ``user_can_view`` throws an exception it safely returns False.

    For example::

      {% if myItem|can_view:request.user %}
        {{ item }}
      {% endif %}
    """
    try:
        return perms.user_can_view(user,item)
    except:
        return False

@register.filter
def can_edit(item,user):
    """
    A filter that acts as a wrapper around ``aristotle_mdr.perms.user_can_edit``.
    Returns true if the user has permission to edit the item, otherwise it returns False.
    If calling ``user_can_edit`` throws an exception it safely returns False.

    For example::

      {% if myItem|can_edit:request.user %}
        {{ item }}
      {% endif %}
    """
    try:
        return perms.user_can_edit(user,item)
    except:
        return False

@register.filter
def can_view_iter(qs,user):
    """
    A filter that is a simple wrapper that applies the ``aristotle_mdr.models.ConceptManager.visible(user)``
    for use in templates. Filtering on a Django ``Queryset`` and passing in the current
    user as the argument returns a list (not a ``Queryset`` at this stage) of only
    the items from the ``Queryset`` the user can view.

    If calling ``can_view_iter`` throws an exception it safely returns an empty list.

    For example::

        {% for item in myItems|can_view_iter:request.user %}
          {{ item }}
        {% endfor %}
    """
    try:
        return qs.visible(user)
    except:
        return []

@register.filter
def islice(itera,slice):
    """
    A duplicate of the django `slice filter`_ that works on iterables as well as lists.

    .. _slice filter: https://docs.djangoproject.com/en/dev/ref/templates/builtins/#slice

    For example, below returns the first 5 items from an iterable::

        {% for item in myItems|slice:":5" %}
          {{ item }}
        {% endfor %}

    """
    try:
        return eval("itera[%s]"%slice)
    except:
        return itera

#http://stackoverflow.com/questions/2047622/how-to-paginate-django-with-other-get-variables
@register.simple_tag
def search(request, pageNumber):
    dict_ = request.GET.copy()
    dict_['page'] = pageNumber
    return dict_.urlencode()

@register.simple_tag
def ifeq(a, b, val):
    return val if a == b else ""

@register.simple_tag
def ternary(condition, a, b):
    """
    A simple ternary tag - it beats verbose if/else tags in templates for simple strings
    If the ``condition`` is 'truthy' return ``a`` otherwise return ``b``. For example::

        <a class="{% ternary item.is_public 'public' 'private' %}">{{item.name}}</a>
    """
    if condition:
        return a
    else:
        return b

@register.simple_tag
def pluralmodel(item,value):
    if value == 1:
        return item.get_verbose_name()
    else:
        return item.get_verbose_name_plural()

@register.filter
def search_paginator(page,mode):
    if mode=="start":
        if page.number <= 5:
            # show 4,5,6 if page is 4, 5,6,7 if page is 5...
            return page.paginator.page_range[:max(5,page.number+2)]
        else:
            return page.paginator.page_range[:3]
    if mode=="middle":
        if page.number > 5 and page.number < page.paginator.num_pages - 5:
            return page.paginator.page_range[page.number-3:page.number+2]
    if mode=="end":
        if page.number > page.paginator.num_pages - 5:
            return page.paginator.page_range[-5:]
        else:
            return page.paginator.page_range[-1:]

#@register.simple_tag
@register.filter
def stateToText(state):
    """
    This tag takes the integer value of a state for a registration status and
    converts it to its text equivilent.
    """
    return MDR.STATES[int(state)]

# Adds a zerowidth space before an em-dash
@register.simple_tag
def zws(string):
    """
    ``zws`` or "zero width space" is used to insert a soft break near em-dashed.
    Since em-dashs are commonly used in Data Element Concept names, this helps them wrap
    in the right places.

    For example::

        <h1>{% zws item.name %}</h1>

    """
    string = string.encode('utf-8','xmlcharrefreplace')
    return string.replace("—","&shy;—")

@register.simple_tag
def adminEdit(item):
    """
    A tag for easily generating the link to an admin page for editing an item. For example::

        <a href="{% adminEdit item %}">Advanced editor for {{item.name}}</a>
    """
    app_name = item._meta.app_label
    return reverse("admin:%s_%s_change"%(app_name,item.url_name().lower()),args=[item.id])

@register.simple_tag
def clone(item):
    """
    A tag for easily generating the link to an admin page for "cloning" an item. For example::

        <a href="{% clone item %}">Clone {{item.name}}</a>
    """
    app_name = item._meta.app_label
    return reverse("admin:%s_%s_add"%(app_name,item.url_name().lower()))+"?clone=%s"%item.id

@register.simple_tag
def aboutLink(item):
    app_name = item._meta.app_label
    return reverse("%s:about"%app_name,args=[item.url_name().lower()])


@register.simple_tag
def itemURL(item):
    app_name = item._meta.app_label
    return reverse("%s:%s"%(app_name,item.template_name()),args=[item.id])

@register.simple_tag
def downloadMenu(item):
    """
    Returns the complete download menu for a partcular item. It accepts the id of
    the item to make a download menu for, and the id must be of an item that can be downloaded,
    otherwise the links will show, but not work.

    For example::

        {% downloadMenu item %}
    """
    from django.conf import settings
    from django.template.loader import get_template
    from django.template import Context
    downloadOpts = getattr(settings, 'ARISTOTLE_DOWNLOADS', "")
    return get_template("aristotle_mdr/helpers/downloadMenu.html").render(
        Context({'item':item,'downloadOptions':downloadOpts,})
        )

@register.simple_tag
def extra_content(extension,item,user):
    try:
        from django.template.loader import get_template
        from django.template import Context
        return get_template(extension+"/concepts/extra_content/"+item.template_name()+".html").render(
            Context({'item':item,'user':user})
        )
    except template.TemplateDoesNotExist:
        return ""
        # there is no extra content for this item, and thats ok.