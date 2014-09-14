#-*- coding: utf-8 -*-

from django import template
from aristotle_mdr import perms
from aristotle_mdr import models as MDR
from django.core.urlresolvers import reverse, resolve
from django.shortcuts import render

register = template.Library()


@register.filter
def can_view(item,user):
    """
    A filter that acts as a wrapper around ``aristotle_mdr.perms.can_view``.
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
    A filter that acts as a wrapper around ``aristotle_mdr.perms.can_edit``.
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
    For example::

        {% for item in myItems|can_view_iter:request.user %}
          {{ item }}
        {% endfor %}
    """

    try:
        return qs.visible(user) #[item for item in itera if perms.user_can_view(user,item)]
    except:
        #Fail safely
        return []

@register.filter
def islice(itera,slice):
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
    If condition is 'truthy' return a otherwise return 'b'
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
    return MDR.STATES[int(state)]

# Adds a zerowidth space before an em-dash
@register.simple_tag
def zws(string):
    string = string.encode('utf-8','xmlcharrefreplace')
    return string.replace("—","&shy;—")

@register.simple_tag
def adminEdit(item):
    app_name = item._meta.app_label
    return reverse("admin:%s_%s_change"%(app_name,item.url_name().lower()),args=[item.id])

@register.simple_tag
def clone(item):
    app_name = item._meta.app_label
    return reverse("admin:%s_%s_add"%(app_name,item.url_name().lower()))+"?clone=%s"%item.id

@register.simple_tag
def aboutLink(item):
    app_name = item._meta.app_label
    return reverse("%s:about"%app_name,args=[item.url_name().lower()])

@register.simple_tag
def downloadMenu(iid):
    from django.conf import settings
    from django.template.loader import get_template
    from django.template import Context
    downloadOpts = getattr(settings, 'ARISTOTLE_DOWNLOADS', "")
    return get_template("aristotle_mdr/helpers/downloadMenu.html").render(
        Context({'iid':iid,'downloadOptions':downloadOpts,})
        )
