import autocomplete_light
autocomplete_light.autodiscover()

from django.conf.urls import include, patterns, url

from aristotle_mdr import views,forms
from django.views.generic import TemplateView

from haystack.query import SearchQuerySet
from haystack.views import search_view_factory

sqs = SearchQuerySet()

urlpatterns = patterns('aristotle_mdr.views',
    url(r'^/?$', TemplateView.as_view(template_name='aristotle_mdr/static/home.html'),name="home"),

    # all the below take on the same form:
    # url(r'^itemType/(?P<iid>\d+)?/?
    # Allowing for a blank ItemId (iid) allows aristotle to redirect to /about/itemtype instead of 404ing
    url(r'^objectclass/(?P<iid>\d+)?/?$', views.objectclass, name='objectClass'),
    #url(r'^objectclass/(?P<iid>\d+)?(?:/(?P<subpage>\w+))?/?$', views.objectclass, name='objectClass'),
    url(r'^property/(?P<iid>\d+)?/?$', views.property, name='property'),
    url(r'^valuedomain/(?P<iid>\d+)?/?$', views.valuedomain, name='valueDomain'),
    url(r'^dataelementconcept/(?P<iid>\d+)?/?$', views.dataelementconcept, name='dataElementConcept'),
    url(r'^dataelement/(?P<iid>\d+)?(?:-[a-z\-]*)?/?$', views.dataelement, name='dataElement'),
    url(r'^registrationauthority/(?P<iid>\d+)/?$', views.registrationauthority, name='registrationAuthority'),
    url(r'^glossary/(?P<iid>\d+)/?$', views.glossaryById, name='glossary_id'),
    url(r'^datatype/(?P<iid>\d+)(?:/(?P<subpage>\w+))?/?$', views.datatype, name='dataType'),
    url(r'^package/(?P<iid>\d+)/?$', views.package, name='package'),
    url(r'^datasetspecification/(?P<iid>\d+)/?$', views.datasetspecification, name='dataSetSpecification'),
    #url(r'^glossary/(?P<slug>\w+)/?$', views.glossaryBySlug, name='glossary_slug'),

    url(r'^workgroup/(?P<iid>\d+)/members/?$', views.workgroupMembers, name='workgroupMembers'),
    url(r'^workgroup/(?P<iid>\d+)(?:/(?P<subpage>\w+))?/?$', views.workgroup, name='workgroup'),


    url(r'^discussions/$', views.discussions, name='discussions'),
    url(r'^item/(?P<item_id>\d+)/?$', views.item, name='item'),
    url(r'^item/(?P<item_id>\d+)/packages/?$', views.itemPackages, name='itemPackages'),
    url(r'^item/(?P<item_id>\d+)/registrationHistory/?$', views.registrationHistory, name='registrationHistory'),

    #url(r'^create/?$', views.item, name='item'),
    url(r'^create/?$', views.allRegistrationAuthorities, name='createList'),
    url(r'^create/objectclass/?$', views.createObjectclass, name='createObjectClass'),
    url(r'^create/property/?$', views.createProperty, name='createProperty'),
    #url(r'^create/datatype/?$', views.createDataType, name='createDataType'),
    url(r'^create/valuedomain/?$', views.createValueDomain, name='createValueDomain'),
    url(r'^create/dataelementconcept$', views.createDataElementConcept, name='createDataElementConcept'),
#    url(r'^create/dataelement$', views.createDataElement, name='createDataElement'),
#    url(r'^create/dataelementconcept$', views.DataElementConceptWizard.as_view()),

    url(r'^download/(?P<downloadType>[a-zA-Z0-9\-]+)/(?P<iid>\d+)/?$', views.download, name='download'),

    url(r'^action/supersede/(?P<iid>\d+)$', views.supersede, name='supersede'),
    url(r'^action/deprecate/(?P<iid>\d+)$', views.deprecate, name='deprecate'),
    url(r'^action/bulkFavourite$', views.bulkFavourite, name='bulkFavourite'),
    url(r'^remove/deFromDss/(?P<de_id>\d+)/(?P<dss_id>\d+)', views.removeDataElementFromDSS, name='removeDataElementFromDSS'),
    url(r'^changestatus/(?P<iid>\d+)$', views.changeStatus, name='changeStatus'),
    url(r'^addWorkgroupMembers/(?P<iid>\d+)$', views.addWorkgroupMembers, name='addWorkgroupMembers'),
    url(r'^remove/WorkgroupRole/(?P<iid>\d+)/(?P<role>\w+)/(?P<userid>\d+)/?$', views.removeWorkgroupRole, name='removeWorkgroupRole'),
    #url(r'^remove/WorkgroupUser/(?P<iid>\d+)/(?P<userid>\d+)$', views.removeWorkgroupUser, name='removeWorkgroupUser'),

    url(r'^account/home/?', views.userHome, name='userHome'),
    url(r'^account/userAdminTools/?', views.userAdminTools, name='userAdminTools'),
    url(r'^account/edit/?', views.userEdit, name='userEdit'),
    url(r'^account/inbox(?:/(?P<folder>all))?/?', views.userInbox, name='userInbox'),
    url(r'^account/favourites/?$', views.userFavourites, name='userFavourites'),
    url(r'^account/workgroups/?$', views.userWorkgroups, name='userWorkgroups'),

    url(r'^account/registrartools/?$', views.userRegistrarTools, name='userRegistrarTools'),
    url(r'^account/registrartools/readyforreview/?$', views.userReadyForReview, name='userReadyForReview'),

    url(r'^registrationauthorities/?$', views.allRegistrationAuthorities, name='allRegistrationAuthorities'),
    url(r'^account/toggleFavourite/(?P<item_id>\d+)/?', views.toggleFavourite, name='toggleFavourite'),

    url(r'^browse(?:/(?P<oc_id>\d+)(?:-[a-z\-]*)?(?:/(?P<dec_id>\d+)(?:-[a-z\-]*)?)?)?/?$', views.browse, name='browse'),

    url(r'^about/site/?$', views.aboutThisSite, name="aboutThisSite"),
    url(r'^about/(?P<template>.+)/?$', views.DynamicTemplateView.as_view(), name="about"),
    url(r'^about/?$', TemplateView.as_view(template_name='aristotle_mdr/static/aristotle_mdr.html'), name="aboutMain"),
    url(r'^help/(?P<template>.+)/?$', views.HelpTemplateView.as_view(), name="help"),
    url(r'^help/?$', TemplateView.as_view(template_name='aristotle_mdr/static/help/help.html'), name="helpMain"),

    url(r'^search/?', search_view_factory(
     view_class=views.PermissionSearchView,
     template='search/search.html',
     searchqueryset=sqs,
     form_class=forms.PermissionSearchForm
     ), name='search'),

    # Things that keep it running
    #url(r'^manage/', include(admin.site.urls)),
)

