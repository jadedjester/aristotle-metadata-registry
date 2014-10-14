import notifications
import autocomplete_light
# import every app/autocomplete_light_registry.py
autocomplete_light.autodiscover()

from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^login/?$', 'django.contrib.auth.views.login'),
    url(r'^logout/?$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^inplaceeditform/', include('inplaceeditform.urls')),
    url('^account/notifications/', include(notifications.urls)),

    url(r'^', include('aristotle_mdr.urls_aristotle',app_name="aristotle_mdr",namespace="aristotle")),

    )

handler403 = 'aristotle_mdr.views.unauthorised'