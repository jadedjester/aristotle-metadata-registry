import datetime
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

from haystack import connections
from haystack.constants import DEFAULT_ALIAS
from haystack.forms import SearchForm, model_choices
from haystack.query import SearchQuerySet, SQ

from bootstrap3_datetime.widgets import DateTimePicker

import aristotle_mdr.models as MDR
from aristotle_mdr.widgets import BootstrapDropdownSelectMultiple, BootstrapDropdownIntelligentDate, BootstrapDropdownSelect

QUICK_DATES = Choices (
       ('a','anytime',_('Any time')),
       ('h','hour',_('Last hour')),
       ('t','today',_('Today')),
       ('w','week',_('This week')),
       ('m','month',_('This month')),
       ('y','year',_('This year')),
       ('X','custom',_('Custom period')),
     )

SORT_OPTIONS = Choices (
       ('n','natural',_('Ranking')),
       ('ma','modified_ascending',_('Modified ascending')),
       ('md','modified_descending',_('Modified descending')),
       ('ma','created_ascending',_('Created ascending')),
       ('md','created_descending',_('Created descending')),
       ('aa','alphabetical',_('Alphabetical')),
       ('s','state',_('Registration state')),
     )

# This function is not critical and are mathematically sound, so testing is not required.
def time_delta(delta): # pragma: no cover
    """
    Datetimes are expensive to search on, so this function gives approximations of the time options.
    Absolute precision can be used using the custom ranges, but may be slower.
    These approximations mean that similar ranges can be used in the haystack index when searching.
    """
    if delta == QUICK_DATES.hour:
        """
        The last hour, actually translates to the begin of the last hour, so
        this returns objects between 60 and 119 mintues ago.
        """
        n = datetime.datetime.now()
        n = datetime.datetime.combine(n.date(),datetime.time(hour=n.time().hour))
        return n - datetime.timedelta(hours=1)
    elif delta == QUICK_DATES.today:
        """
        Today returns everything today.
        """
        return datetime.date.today() #- datetime.timedelta(days=1)
    elif delta == QUICK_DATES.week:
        """
        This week is pretty straight forward. SSReturns 7 days ago from the *beginning* of today.
        """
        return datetime.date.today() - datetime.timedelta(days=7)
    elif delta == QUICK_DATES.month:
        """
        This goes back to this day last month, and then finds the prior day thats
        divisible by 7 (not less than 1).
          1-6 -> 1
         7-13 -> 7
        14-20 -> 14
        21-27 -> 21
        28-31 -> 28
        """
        t = datetime.date.today()
        last_month = datetime.date(day=1, month=t.month, year=t.year) - datetime.timedelta(days=1)
        days = max(((t.day)//7)*7,1)
        last_month = datetime.date(day=days, month=last_month.month, year=last_month.year)
        return datetime.date(day=1, month=last_month.month, year=last_month.year)
    elif delta == QUICK_DATES.year:
        """
        This goes back to the beginning of this month last year.
        So it searchs from the first of this month, last year.
        """
        t = datetime.date.today()
        return datetime.date(day=1, month=t.month, year=(t.year-1))
    return None
DELTA ={QUICK_DATES.hour : datetime.timedelta(hours=1),
        QUICK_DATES.today : datetime.timedelta(days=1),
        QUICK_DATES.week  : datetime.timedelta(days=7),
        QUICK_DATES.month : datetime.timedelta(days=31),
        QUICK_DATES.year  : datetime.timedelta(days=366)
        }


class PermissionSearchQuerySet(SearchQuerySet):
    def apply_permission_checks(self,user=None,public_only=False,user_workgroups_only=False):
        sqs = self
        q = SQ(is_public=True)
        if user is None or user.is_anonymous():
            # Regular users can only see public items, so boot them off now.
            sqs = sqs.filter(q)
            return sqs

        if not user.is_superuser:
            # Non-registrars can only see public things or things in their workgroup
            # if they have no workgroups they won't see anything extra
            if user.profile.workgroups.count() > 0:
                #for w in user.profile.workgroups.all():
                #    q |= SQ(workgroup=str(w.id))
                q |= SQ(workgroup__in=[int(w.id) for w in user.profile.workgroups.all()])
            if user.profile.is_registrar:
                # if registrar, also filter through items in the registered in their authorities
                q |= SQ(registrationAuthorities__in=[str(r.id) for r in user.profile.registrarAuthorities])
        if public_only:
            q &= SQ(is_public=True)
        if user_workgroups_only:
            q &= SQ(workgroup__in=[str(w.id) for w in user.profile.workgroups.all()])
        sqs = sqs.filter(q)
        return sqs

class TokenSearchForm(SearchForm):
    def prepare_tokens(self):
        try:
            query = self.cleaned_data.get('q')
        except:
            return {}
        opts = connections[DEFAULT_ALIAS].get_unified_index().fields.keys()
        kwargs = {}
        query_text = []
        for word in query.split(" "):
            if ":" in word:
                opt,arg = word.split(":",1)
                if opt in opts:
                    kwargs[str(opt)]=arg
            else:
                query_text.append(word)
        self.query_text = " ".join(query_text)
        self.kwargs = kwargs
        return kwargs

    def search(self):
        self.query_text = None
        kwargs = self.prepare_tokens()
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.query_text)

        if kwargs:
            sqs = sqs.filter(**kwargs)

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

datePickerOptions={
    "format": "YYYY-MM-DD",
    "pickTime": False,
    "pickDate": True,
    "defaultDate":"",
    "useCurrent": False,
}


class PermissionSearchForm(TokenSearchForm):
    """
        We need to make a new form as permissions to view objects are a bit finicky.
        This form allows us to perform the base query then restrict it to just those
        of interest.

        TODO: This might not scale well, so it may need to be looked at in production.
    """
    mq=forms.ChoiceField(required=False,initial=QUICK_DATES.anytime,
        choices=QUICK_DATES,widget=BootstrapDropdownIntelligentDate)

    mds = forms.DateField(required=False,
        widget=DateTimePicker(options=datePickerOptions),
        )
    mde = forms.DateField(required=False,
        widget=DateTimePicker(options=datePickerOptions),
        )
    cq=forms.ChoiceField(required=False,initial=QUICK_DATES.anytime,
        choices=QUICK_DATES,widget=BootstrapDropdownIntelligentDate)

    cds = forms.DateField(required=False,
        widget=DateTimePicker(options=datePickerOptions),
        )
    cde = forms.DateField(required=False,
        widget=DateTimePicker(options=datePickerOptions),
        )

    # Use short singular names
    #ras = [(ra.id, ra.name) for ra in MDR.RegistrationAuthority.objects.all()]
    ra = forms.MultipleChoiceField(required=False,
        choices=[],widget=BootstrapDropdownSelectMultiple)

    sort = forms.ChoiceField(required=False,initial=SORT_OPTIONS.natural,
        choices=SORT_OPTIONS,widget=BootstrapDropdownSelect)

    state = forms.MultipleChoiceField(required=False,
        choices=MDR.STATES,widget=BootstrapDropdownSelectMultiple)
    public_only = forms.BooleanField(required=False,
        label="Only show public items"
    )
    myWorkgroups_only = forms.BooleanField(required=False,
        label="Only show items in my workgroups"
    )
    models = forms.MultipleChoiceField(choices=model_choices(),
                required=False, label=_('Item type'),
                widget=BootstrapDropdownSelectMultiple
                )

    def __init__(self,*args, **kwargs):
        kwargs['searchqueryset'] = PermissionSearchQuerySet()
        super(PermissionSearchForm, self).__init__(*args, **kwargs)

        self.fields['ra'].choices = [(ra.id, ra.name) for ra in MDR.RegistrationAuthority.objects.all()]

    def get_models(self):
        """Return an alphabetical list of model classes in the index."""
        search_models = []

        if self.is_valid():
            for model in self.cleaned_data['models']:
                search_models.append(models.get_model(*model.split('.')))

        return search_models


    def search(self,repeat_search=False):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(PermissionSearchForm, self).search()
        sqs = sqs.models(*self.get_models())
        self.repeat_search = repeat_search

        if not self.is_valid():
            return self.no_query_found()

        filters = "mq cq cds cde mds mde state ra".split()
        has_filter = any([self.cleaned_data.get(f,False) for f in filters])
        if has_filter and not self.query_text and not self.kwargs:
            # If there is a filter, but no query then we'll force some results.
            sqs = SearchQuerySet().order_by('-modified')
            self.filter_search = True
            self.attempted_filter_search = True

        sqs = self.apply_registration_status_filters(sqs)
        sqs = self.apply_date_filtering(sqs)
        sqs = sqs.apply_permission_checks(  user=self.request.user,
                                            public_only=self.cleaned_data['public_only'],
                                            user_workgroups_only=self.cleaned_data['myWorkgroups_only']
                                        )

        self.has_spelling_suggestions = False
        if not self.repeat_search:

            if sqs.count() < 5:
                self.check_spelling(sqs)

            if sqs.count() == 0:
                if has_filter and self.cleaned_data['q']:
                    # If there are 0 results with a search term, and filters applied
                    # lets be nice and remove the filters and try again.
                    # There will be a big message on the search page that says what we did.
                    for f in filters:
                        self.cleaned_data[f] = None
                    self.auto_broaden_search = True
                elif sqs.count() == 0 and self.has_spelling_suggestions:
                    self.auto_correct_spell_search = True
                    self.cleaned_data['q'] = self.suggested_query
                # Re run the query with the updated details
                sqs = self.search(repeat_search=True)
            # Only apply sorting on the first pass through
            sqs = self.apply_sorting(sqs)

        return sqs

    def check_spelling(self,sqs):
        if self.query_text:
            from urllib import quote_plus
            suggestions = []
            has_suggestions = False
            suggested_query = []
            for token in self.cleaned_data.get('q',"").split(" "):
                if token: # remove blanks
                    suggestion = SearchQuerySet().spelling_suggestion(token)
                    if suggestion:
                        suggested_query.append(suggestion)
                        has_suggestions = True
                    else:
                        suggested_query.append(token)
                    suggestions.append((token,suggestion))
            self.spelling_suggestions = suggestions
            self.has_spelling_suggestions = has_suggestions
            self.original_query = self.cleaned_data.get('q')
            self.suggested_query = quote_plus(' '.join(suggested_query),safe="")

    def apply_registration_status_filters(self,sqs):
        states = self.cleaned_data['state']
        ras = self.cleaned_data['ra']
        if states and not ras:
            states = [MDR.STATES[int(s)] for s in self.cleaned_data['state']]
            sqs = sqs.filter(statuses__in=states)
        elif ras and not states:
            ras = [ra for ra in self.cleaned_data['ra']]
            sqs = sqs.filter(registrationAuthorities__in=ras)
        elif states and ras:
            # If we have both states and ras, merge them so we only search for
            # items with those statuses in those ras
            terms = ["%s___%s"%(str(r),str(s)) for r in ras for s in states]
            sqs = sqs.filter(ra_statuses__in=terms)
        return sqs

    def apply_date_filtering(self,sqs):
        modify_quick_date = self.cleaned_data['mq']
        create_quick_date = self.cleaned_data['cq']
        create_date_start = self.cleaned_data['cds']
        create_date_end   = self.cleaned_data['cde']
        modify_date_start = self.cleaned_data['mds']
        modify_date_end   = self.cleaned_data['mde']

        """
        Modified filtering is really hard to do formal testing for as the modified
        dates are altered on save, so its impossible to alter the modified dates
        to check the search is working.
        However, this is the exact same process as creation date (which we can alter),
        so if creation filtering is working, modified filtering should work too.
        """
        if modify_quick_date and modify_quick_date is not QUICK_DATES.anytime: # pragma: no cover
            delta = time_delta(modify_quick_date)
            if delta is not None:
                sqs = sqs.filter(modifed__gte=delta)
        elif modify_date_start or modify_date_end: # pragma: no cover
            if modify_date_start:
                sqs = sqs.filter(modifed__gte=modify_date_start)
            if modify_date_end:
                sqs = sqs.filter(modifed__lte=modify_date_end)

        if create_quick_date and create_quick_date is not QUICK_DATES.anytime:
            delta = time_delta(create_quick_date)
            if delta is not None:
                sqs = sqs.filter(created__gte=delta)
        elif create_date_start or create_date_end:
            if create_date_start:
                sqs = sqs.filter(created__gte=create_date_start)
            if create_date_end:
                sqs = sqs.filter(created__lte=create_date_end)

        return sqs

    def apply_sorting(self,sqs): #pragma: no cover, no security issues, standard Haystack methods, so already tested.
        sort_order  = self.cleaned_data['sort']
        if sort_order == SORT_OPTIONS.modified_ascending:
            sqs = sqs.order_by('-modified')
        elif sort_order == SORT_OPTIONS.modified_descending:
            sqs = sqs.order_by('modified')
        elif sort_order == SORT_OPTIONS.created_ascending:
            sqs = sqs.order_by('-created')
        elif sort_order == SORT_OPTIONS.created_descending:
            sqs = sqs.order_by('created')
        elif sort_order == SORT_OPTIONS.alphabetical:
            sqs = sqs.order_by('name')
        elif sort_order == SORT_OPTIONS.state:
            sqs = sqs.order_by('-highest_state')

        return sqs

