from django import forms
from django.db.models import Q
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.admin.filters import RelatedFieldListFilter
import aristotle_mdr.models as MDR
import aristotle_mdr.forms as MDRForms
from aristotle_mdr import perms
from django.core.urlresolvers import reverse
import reversion
from reversion_compare.admin import CompareVersionAdmin


# Thanks http://stackoverflow.com/questions/6727372/
class RegistrationAuthoritySelect(forms.Select):
    def render(self, name, value, attrs=None, choices=()):
        if value is not None:
            attrs['disabled']='disabled'
        return super(RegistrationAuthoritySelect, self).render(name, value, attrs, choices)

class StatusInlineForm(forms.ModelForm):
    registrationAuthority = forms.ModelChoiceField(label='Registration Authority',queryset=MDR.RegistrationAuthority.objects,widget=RegistrationAuthoritySelect)
    class Meta:
        model = MDR.Status

"""
Inline editor for registration status records
"""
class StatusInline(admin.TabularInline):
    model = MDR.Status
    form = StatusInlineForm
    extra=0

    """
    The default queryset will return all objects of a given type.
    This limits the returned Status Records to only those where
    they are in a Registration Authority in which the current user
    has permission to change the status of objects.
    """
    def queryset(self, request):
        qs = super(StatusInline, self).queryset(request)
        if not request.user.is_superuser:
            ra = [r for r in request.user.profile.registrationAuthorities.all()
                    if request.user.has_perm('aristotle_mdr.promote_in_{name}'.format(name=r.name))
                 ]
            qs = qs.filter(registrationAuthority__in=ra)
        return qs

    def has_change_permission(self, request,obj=None):
        if obj is not None and perms.user_can_change_status(request.user,obj):
            return True
        return super(StatusInline, self).has_change_permission(request,obj=None)
    def has_add_permission(self, request):
        if True in (request.user.has_perm('aristotle_mdr.promote_in_{name}'.format(name=r.name))
                for r in request.user.profile.registrationAuthorities.all()
                ):
            return True
        return super(StatusInline, self).has_add_permission(request)
    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
        #    if request.user.has_perm('aristotle_mdr.promote_in_{name}'.format(name=obj.registrationAuthority.name):
            return () #('concept','registrationAuthority')
        else:
            #    return self.fields
            return ()

class WorkgroupFilter(RelatedFieldListFilter):
    def __init__(self, field, request, *args, **kwargs):
        if not request.user.is_superuser:
            wg_ids = [w.id for w in request.user.profile.myWorkgroups.all()]

            #Limit the choices on the field
            field.rel.limit_choices_to = {'id__in': wg_ids}
        #Let the RelatedFieldListFilter do its magic
        super(WorkgroupFilter, self).__init__(field, request, *args, **kwargs)

class WorkgroupAdmin(CompareVersionAdmin):
    def queryset(self, request):
        qs = super(WorkgroupAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return request.user.profile.myWorkgroups.all()


class ConceptAdmin(CompareVersionAdmin):
    class Media:
        js = [
                '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            ]

    def compare_workgroup(self, obj_compare):
        return ""

    form = MDRForms.admin.AdminConceptForm
    list_display = ['name', 'description','created','modified', 'workgroup','is_public','is_locked','readyToReview']#,'status']
    list_filter = ['created','modified',('workgroup',WorkgroupFilter)] #,'statuses']
    search_fields = ['name','synonyms']
    inlines = [StatusInline, ]

    change_list_template = "admin/change_list_filter_sidebar.html"
    change_list_filter_template = "admin/filter_listing.html"
    date_hierarchy='created'# ,'modified']

    fieldsets = [
        (None,              {'fields': ['name','description','workgroup']}),
        ('Additional names',{
                'classes':('grp-collapse grp-closed',),
                'fields': ['synonyms','shortName','version',]
            }),
        #('Registry',        {'fields': ['workgroup']}),
        ('Relationships',   {
                'classes':('grp-collapse grp-closed',),
                'fields': ['superseded_by','deprecated'],
            })
    ]

    raw_id_fields = ('workgroup',)
    autocomplete_lookup_fields = {'fk':['workgroup',]}
    light_autocomplete_lookup_fields = {
        'fk': [],
    }
    actions_on_top = True; actions_on_bottom = False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "workgroup":
            kwargs['queryset'] = request.user.profile.myWorkgroups.all()
            kwargs['initial'] = request.user.profile.activeWorkgroup
        return super(ConceptAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        # Thanks: http://stackoverflow.com/questions/6321916
        # Thanks: http://stackoverflow.com/questions/2683689
        conceptForm = super(ConceptAdmin, self).get_form(request, obj, **kwargs)
        class ModelFormMetaClass(conceptForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                kwargs['auto_fields'] = self.light_autocomplete_lookup_fields
                return conceptForm(*args, **kwargs)
        return ModelFormMetaClass

    def has_change_permission(self, request,obj=None):
        if obj is not None:
            if perms.user_can_edit(request.user,obj):
                return True
            if perms.user_can_change_status(request.user,obj):
                return True
            else:
                return super(ConceptAdmin, self).has_change_permission(request,obj=None)
        else:
            return True
    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super(ConceptAdmin, self).has_delete_permission(request,obj=None)
        else:
            return perms.user_can_edit(request.user,obj) and not obj.is_registered

    def get_queryset(self, request):
        queryset = super(ConceptAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            """
            workgroups=request.user.profile.workgroups.all()
            # Get all objects in the users workgroups
            in_wg = queryset.filter(workgroup__in=workgroups)
            in_ra = []
            #Check for objects registered in the users RAs
            ra = (r for r in request.user.profile.registrationAuthorities.all()
                    if request.user.has_perm('aristotle_mdr.view_registered_in_{name}'.format(name=r.name)))
            s = MDR.Status.objects.filter(registrationAuthority__in=ra)
            in_ra = queryset.filter(statuses__in=s)
            # TODO: Change to respect RA public guidelines
            # This will require changing how we determine whats "public" and probably adding a cache flag to the model.
            # (i for i in queryset if i.is_public)
            public = MDR.Status.objects.filter(state__in=[MDR.STATES.standard,MDR.STATES.preferred])
            is_public = queryset.filter(statuses__in=public)
            queryset = in_wg | in_ra | is_public
            """
            #queryset.qs.filter(registrationAuthority__in=ra)
            if not self.has_change_permission(request):
                queryset = queryset.none()
            else:
                return queryset.editable_slow(request.user).all()
        return queryset

    # On save or add, redirect to the live page.
    # Implementing this would be nice:
    #      http://www.szotten.com/david/custom-redirects-in-the-django-admin.html
    def response_add(self, request, obj, post_url_continue=None):
        response = super(ConceptAdmin, self).response_add(request, obj)
        if request.POST.has_key('_save') and post_url_continue is None:
            response['location'] = reverse("aristotle:item",args=(obj.id,))
        return response
    def response_change(self, request, obj, post_url_continue=None):
        response = super(ConceptAdmin, self).response_change(request, obj)
        if request.POST.has_key('_save'):
            response['location'] = reverse("aristotle:item",args=(obj.id,))
        return response


class DataElementAdmin(ConceptAdmin):
    fieldsets = ConceptAdmin.fieldsets + [
            ('Components', {'fields': ['dataElementConcept','valueDomain']}),
    ]
    raw_id_fields = ConceptAdmin.raw_id_fields + ('dataElementConcept','valueDomain')
    light_autocomplete_lookup_fields = {
        'fk': [
            ('dataElementConcept',MDR.DataElementConcept ),
            ('valueDomain',MDR.ValueDomain ),
            ] +ConceptAdmin.light_autocomplete_lookup_fields['fk'],
    }

class DataElementConceptAdmin(ConceptAdmin):
    fieldsets = ConceptAdmin.fieldsets + [
            ('Components', {'fields': ['objectClass','property']}),
    ]
    #raw_id_fields = ConceptAdmin.raw_id_fields + ('objectClass','property',)
    light_autocomplete_lookup_fields = {
        'fk': [
            ('objectClass',MDR.ObjectClass ),
            ('property',MDR.Property ),
            ] +ConceptAdmin.light_autocomplete_lookup_fields['fk'],
    }

class ObjectClassAdmin(ConceptAdmin):       pass
class ConceptualDomainAdmin(ConceptAdmin):  pass
class PackageAdmin(ConceptAdmin):           pass
class PropertyAdmin(ConceptAdmin):          pass

class CodeValueInline(admin.TabularInline):
    form = MDRForms.PermissibleValueForm
    #fields = ("value","meaning")
    sortable_field_name = "order"
    extra = 1

class PermissibleValueInline(CodeValueInline):
    model = MDR.PermissibleValue
class SupplementaryValueInline(CodeValueInline):
    model = MDR.SupplementaryValue


class ValueDomainAdmin(ConceptAdmin):
    fieldsets = ConceptAdmin.fieldsets + [
            ('Representation', {'fields': ['format','maximumLength','unitOfMeasure','dataType']}),
    ]
    inlines = ConceptAdmin.inlines + [PermissibleValueInline,SupplementaryValueInline]

class GlossaryAlternateDefinitionInline(admin.TabularInline):
    model = MDR.GlossaryAdditionalDefinition
    extra=0

class GlossaryItemAdmin(admin.ModelAdmin):
    model = MDR.GlossaryItem
    inlines = [GlossaryAlternateDefinitionInline]

class RegistrationAuthorityAdmin(admin.ModelAdmin):
    list_display = ['name', 'description','created','modified']
    list_filter = ['created','modified',]
    fieldsets = [
        (None,              {'fields': ['name','description']}),
        ('Visibility and control',              {'fields': ['locked_state','public_state',]}),
        ('Status descriptions',
            {'fields': ['notprogressed','incomplete','candidate','recorded','qualified','standard','preferred','superseded','retired',]}),
    ]


# Register your models here.
admin.site.register(MDR.ConceptualDomain,ConceptualDomainAdmin)
admin.site.register(MDR.DataElement,DataElementAdmin)
admin.site.register(MDR.DataElementConcept,DataElementConceptAdmin)
admin.site.register(MDR.GlossaryItem,GlossaryItemAdmin)
admin.site.register(MDR.Package,PackageAdmin)
admin.site.register(MDR.Property,PropertyAdmin)
admin.site.register(MDR.ObjectClass,ObjectClassAdmin)
admin.site.register(MDR.RegistrationAuthority,RegistrationAuthorityAdmin)
admin.site.register(MDR.ValueDomain,ValueDomainAdmin)
admin.site.register(MDR.Workgroup,WorkgroupAdmin)


class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ['name', 'measure', 'created','modified']
    search_fields = ['name','measure']
    list_filter = ['measure', 'created','modified']

admin.site.register(MDR.UnitOfMeasure,UnitOfMeasureAdmin)
admin.site.register(MDR.Measure)
admin.site.register(MDR.DataType)
#admin.site.register(MDR.)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class PossumProfileInline(admin.StackedInline):
    model = MDR.PossumProfile
    can_delete = False
    verbose_name_plural = 'Membership details'
    filter_horizontal = ('workgroups','registrationAuthorities')

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = [PossumProfileInline, ]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

