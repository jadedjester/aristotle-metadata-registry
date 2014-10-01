from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.utils import timezone
import datetime
import urllib
from django.contrib.auth.models import User

from aristotle_mdr.perms import user_can_view, user_can_edit, user_in_workgroup, user_is_workgroup_manager, user_can_change_status
from aristotle_mdr import perms
import aristotle_mdr.forms as MDRForms # Treble-one seven nine
import aristotle_mdr.models as MDR # Treble-one seven nine

from haystack.views import SearchView
from haystack.query import SearchQuerySet

import cStringIO as StringIO
import xhtml2pdf.pisa as pisa
from django.template.loader import get_template
from django.template import Context
import cgi

PAGES_PER_RELATED_ITEM = 15

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result,encoding='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))

class DynamicTemplateView(TemplateView):
    def get_template_names(self):
        return ['aristotle_mdr/static/%s.html' % self.kwargs['template']]

class HelpTemplateView(TemplateView):
    def get_template_names(self):
        return ['aristotle_mdr/static/help/%s.html' % self.kwargs['template']]

def get_if_user_can_view(objtype,user,iid):
    item = get_object_or_404(objtype,pk=iid)
    if user_can_view(user,item):
        return item
    else:
        return False

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

def render_if_user_can_view(*args,**kwargs):
    return render_if_condition_met(user_can_view,*args,**kwargs)

@login_required
def render_if_user_can_edit(*args,**kwargs):
    return render_if_condition_met(user_can_edit,*args,**kwargs)

def download(request,downloadType,iid=None):
    item = MDR._concept.objects.get_subclass(pk=iid)
    item = get_if_user_can_view(item.__class__,request.user, iid)
    if not item:
        if request.user.is_anonymous():
            return redirect('/accounts/login?next=%s' % request.path)
        else:
            raise PermissionDenied
    p,t = item.template.split("/",1)
    template = "%s/%s/%s"%(p,downloadType,t)

    if downloadType=="pdf":
        subItems = item.getPdfItems
        return render_to_pdf(template,
            {'item':item,
             'items':subItems,
             'tableOfContents':len(subItems)>0,
             'view':request.GET.get('view','').lower(),
             'pagesize':request.GET.get('pagesize','A4'),
            }
        )

    raise Http404

# This has turned into a "god-function" and should be refactored.
def render_if_condition_met(condition,objtype,request,iid=None,subpage=None):
    if iid is None:
        app_name = objtype._meta.app_label
        return redirect(reverse("%s:dynamic"%app_name,args=["".join(objtype._meta.verbose_name.title().lower().split())]))
    item = get_object_or_404(objtype,pk=iid).item
    if not condition(request.user, item):
        if request.user.is_anonymous():
            return redirect('/accounts/login?next=%s' % request.path)
        else:
            raise PermissionDenied

    # We add a user_can_edit flag in addition to others as we have odd rules around who can edit objects.
    isFavourite = request.user.is_authenticated () and request.user.profile.isFavourite(item.id)
    """
    if subpage=="related":
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
        related_items = item.relatedItems(request.user)
        paginator = Paginator(related_items, PAGES_PER_RELATED_ITEM)

        page = request.GET.get('page')
        try:
            related_items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            related_items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            related_items = paginator.page(paginator.num_pages)

        return render(request,"aristotle_mdr/relatedItems.html",
            {'item':item,
             'relatedItems':related_items,}
            )
    else:
    Lets disable the related page for the time being
    Only a handful of Object classes will be impacted.
    """
    from reversion.revisions import default_revision_manager
    last_edit = default_revision_manager.get_for_object_reference(
            item.__class__,
            item.pk,
        ).first()
    return render(request,item.template,
        {'item':item,
         'user_can_edit':user_can_edit(request.user,item),
         'view':request.GET.get('view','').lower(),
         'isFavourite': isFavourite,
         'last_edit': last_edit
            }
        )

def itemPackages(request, item_id):
    item = get_if_user_can_view(MDR._concept,request.user,item_id)
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    packages = item.packages.all().visible(request.user)
    paginator = Paginator(packages, PAGES_PER_RELATED_ITEM)
    page = request.GET.get('page')
    try:
        packages = paginator.page(page)
    except PageNotAnInteger:
        packages = paginator.page(1)
    except EmptyPage:
        packages = paginator.page(paginator.num_pages)

    return render(request,"aristotle_mdr/relatedPackages.html",
        {'item':item.item,
         'packages':packages,}
        )

def registrationHistory(request, item_id):
    item = get_if_user_can_view(MDR._concept,request.user,item_id)
    from reversion.revisions import default_revision_manager
    history = []
    for s in item.statuses.all():
        past = default_revision_manager.get_for_object(s)
        history.append((s,past))
    return render(request,"aristotle_mdr/registrationHistory.html",
            {'item':item,
             'user_can_edit':False,
             'history': history
                }
            )

def item(request, item_id):
    return render_if_user_can_view(MDR._concept,request,item_id)

def unauthorised(request, path=''):
    if request.user.is_anonymous():
        return render(request,"401.html",{"path":path,"anon":True,},status=401)
    else:
        return render(request,"403.html",{"path":path,"anon":True,},status=403)

def objectclass(*args,**kwargs):
    return render_if_user_can_view(MDR.ObjectClass,*args,**kwargs)

def valuedomainPermissibleValue(*args,**kwargs):
    return render_if_user_can_view(MDR.ValueDomain,*args,**kwargs)

def valuedomain(*args,**kwargs):
    return render_if_user_can_view(MDR.ValueDomain,*args,**kwargs)

def property(*args,**kwargs):
    return render_if_user_can_view(MDR.Property,*args,**kwargs)

def dataelementconcept(*args,**kwargs):
    return render_if_user_can_view(MDR.DataElementConcept,*args,**kwargs)

def dataelement(*args,**kwargs):
    return render_if_user_can_view(MDR.DataElement,*args,**kwargs)

def datatype(*args,**kwargs):
    return render_if_user_can_view(MDR.DataType,*args,**kwargs)
def unitofmeasure(*args,**kwargs):
    return render_if_user_can_view(MDR.UnitOfMeasure,*args,**kwargs)

def package(*args,**kwargs):
    return render_if_user_can_view(MDR.Package,*args,**kwargs)

@login_required
def workgroup(request, iid):
    wg = get_object_or_404(MDR.Workgroup,pk=iid)
    if not user_in_workgroup(request.user,wg):
        raise PermissionDenied
    renderDict = {"item":wg,"workgroup":wg,"user_is_admin":user_is_workgroup_manager(request.user,wg)}
    renderDict['recent'] = MDR._concept.objects.filter(workgroup=iid).select_subclasses().order_by('-modified')[:5]
    page = render(request,wg.template,renderDict)
    return page

@login_required
def workgroupItems(request, iid):
    wg = get_object_or_404(MDR.Workgroup,pk=iid)
    if not user_in_workgroup(request.user,wg):
        raise PermissionDenied
    renderDict = {"item":wg,"workgroup":wg,"user_is_admin":user_is_workgroup_manager(request.user,wg)}
    renderDict['items'] = MDR._concept.objects.filter(workgroup=iid).select_subclasses()
    page = render(request,"aristotle_mdr/workgroupItems.html",renderDict)
    return page

@login_required
def workgroupMembers(request, iid):
    wg = get_object_or_404(MDR.Workgroup,pk=iid)
    renderDict = {"item":wg,"workgroup":wg,"user_is_admin":user_is_workgroup_manager(request.user,wg)}
    if not user_in_workgroup(request.user,wg):
        raise PermissionDenied
    return render(request,"aristotle_mdr/workgroupMembers.html",renderDict)

@login_required
def discussions(request):
    #Show all discussions for all of a users workgroups
    page = render(request,"aristotle_mdr/discussions/all.html",{
        'discussions':request.user.profile.discussions
        })
    return page

@login_required
def discussionsWorkgroup(request,wgid):
    wg = get_object_or_404(MDR.Workgroup,pk=wgid)
    if not request.user.has_perm('aristotle_mdr.view_in_{wg}'.format(wg=wg.name)):
        raise PermissionDenied
    #Show all discussions for a workgroups
    page = render(request,"aristotle_mdr/discussions/workgroup.html",{
        'workgroup':wg,
        'discussions':MDR.DiscussionPost.objects.filter(workgroup=wg)
        })
    return page

@login_required
def discussionsPost(request,pid):
    post = get_object_or_404(MDR.DiscussionPost,pk=pid)
    if not request.user.has_perm('aristotle_mdr.view_in_{wg}'.format(wg=post.workgroup.name)):
        raise PermissionDenied
    #Show all discussions for a workgroups
    comment_form = MDRForms.DiscussionCommentForm(initial={'post':pid})
    page = render(request,"aristotle_mdr/discussions/post.html",{
        'workgroup':post.workgroup,
        'post':post,
        'comment_form':comment_form
        })
    return page

@login_required
def discussionsPostToggle(request,pid):
    post = get_object_or_404(MDR.DiscussionPost,pk=pid)
    if not request.user.has_perm('aristotle_mdr.view_in_{wg}'.format(wg=post.workgroup.name)):
        raise PermissionDenied
    post.closed = not post.closed
    post.save()
    return HttpResponseRedirect(reverse("aristotle:discussionsPost",args=[post.pk]))

@login_required
def discussionsNew(request):
    if request.method == 'POST': # If the form has been submitted...
        form = MDRForms.DiscussionNewPostForm(request.POST,user=request.user) # A form bound to the POST data
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new = MDR.DiscussionPost(
                workgroup = form.cleaned_data['workgroup'],
                title = form.cleaned_data['title'],
                body = form.cleaned_data['body'],
                author = request.user,
            )
            new.save()
            new.relatedItems = form.cleaned_data['relatedItems']
            return HttpResponseRedirect(reverse("aristotle:discussionsPost",args=[new.pk]))
    else:
        initial = {}
        if request.GET.get('workgroup') and request.user.profile.myWorkgroups.filter(id=request.GET.get('workgroup')).exists():
            initial={'workgroup':request.GET.get('workgroup')}
        form = MDRForms.DiscussionNewPostForm(user=request.user,initial=initial)
    return render(request,"aristotle_mdr/discussions/new.html",
            {"item":item,
             "form":form,
                }
            )

@login_required
def discussionsPostNewComment(request,pid):
    post = get_object_or_404(MDR.DiscussionPost,pk=pid)
    if not request.user.has_perm('aristotle_mdr.view_in_{wg}'.format(wg=post.workgroup.name)):
        raise PermissionDenied
    if request.method == 'POST':
        form = MDRForms.DiscussionCommentForm(request.POST)
        if form.is_valid():
            new = MDR.DiscussionComment(
                post = post,
                body = form.cleaned_data['body'],
                author = request.user,
            )
            new.save()
            return HttpResponseRedirect(reverse("aristotle:discussionsPost",args=[new.post.pk])+"#comment_%s"%new.id)
    else:
        form = MDRForms.DiscussionCommentForm(initial={'post':pid})
    return render(request,"aristotle_mdr/discussions/new.html",{"form":form,})

@login_required
def discussionsDeleteComment(request,cid):
    comment = get_object_or_404(MDR.DiscussionComment,pk=cid)
    post = comment.post
    if not perms.user_can_alter_comment(request.user,comment):
        raise PermissionDenied
    comment.delete()
    return HttpResponseRedirect(reverse("aristotle:discussionsPost",args=[post.pk]))

@login_required
def discussionsDeletePost(request,pid):
    post = get_object_or_404(MDR.DiscussionPost,pk=pid)
    workgroup = post.workgroup
    if not perms.user_can_alter_post(request.user,post):
        raise PermissionDenied
    post.comments.all().delete()
    post.delete()
    return HttpResponseRedirect(reverse("aristotle:discussionsWorkgroup",args=[workgroup.pk]))

@login_required
def discussionsEditComment(request,cid):
    comment = get_object_or_404(MDR.DiscussionComment,pk=cid)
    post = comment.post
    if not perms.user_can_alter_comment(request.user,comment):
        raise PermissionDenied
    if request.method == 'POST':
        form = MDRForms.DiscussionCommentForm(request.POST)
        if form.is_valid():
            comment.body = form.cleaned_data['body']
            comment.save()
            return HttpResponseRedirect(reverse("aristotle:discussionsPost",args=[comment.post.pk])+"#comment_%s"%comment.id)
    else:
        form = MDRForms.DiscussionCommentForm(instance=comment)

    return render(request,"aristotle_mdr/discussions/edit_comment.html",{
        'post':post,
        'comment_form':form})

@login_required
def discussionsEditPost(request,pid):
    post = get_object_or_404(MDR.DiscussionPost,pk=pid)
    if not perms.user_can_alter_post(request.user,post):
        raise PermissionDenied
    if request.method == 'POST': # If the form has been submitted...
        form = MDRForms.DiscussionEditPostForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            # process the data in form.cleaned_data as required
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            post.save()
            post.relatedItems = form.cleaned_data['relatedItems']
            return HttpResponseRedirect(reverse("aristotle:discussionsPost",args=[post.pk]))
    else:
        form = MDRForms.DiscussionEditPostForm(instance=post)
    return render(request,"aristotle_mdr/discussions/edit.html",{"form":form,'post':post})

@login_required
def userHome(request):
    page = render(request,"aristotle_mdr/user/userHome.html",{"item":request.user})
    return page

@login_required
def userInbox(request,folder=None):
    if folder is None:
        # By default show only unread
        folder='unread'
    folder=folder.lower()
    if folder == 'unread':
        notices = request.user.notifications.unread().all()
    elif folder == "all" :
        notices = request.user.notifications.all()
    page = render(request,"aristotle_mdr/user/userInbox.html",
        {"item":request.user,"notifications":notices,'folder':folder})
    return page

@login_required
def userAdminTools(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    page = render(request,"aristotle_mdr/user/userAdminTools.html",{"item":request.user})
    return page

@login_required
def userEdit(request):
    if request.method == 'POST': # If the form has been submitted...
        form = MDRForms.UserSelfEditForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            # process the data in form.cleaned_data as required
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            return HttpResponseRedirect('/account/home')
    else:
        form = MDRForms.UserSelfEditForm({
            'first_name':request.user.first_name,
            'last_name':request.user.last_name,
            'email':request.user.email,
            })
    return render(request,"aristotle_mdr/user/userEdit.html",
            {"item":item,
             "form":form,
                }
            )

@login_required
def userFavourites(request):
    page = render(request,"aristotle_mdr/user/userFavourites.html",
        {'help':request.GET.get("help",False),
        'favourite':request.GET.get("favourite",False),
        }
    )
    return page

@login_required
def userRegistrationAuthorities(request,iid):
    pass

@login_required
def userRegistrarTools(request):
    if not request.user.profile.is_registrar:
        raise PermissionDenied
    page = render(request,"aristotle_mdr/user/userRegistrarTools.html")
    return page

@login_required
def userReadyForReview(request):
    if not request.user.profile.is_registrar:
        raise PermissionDenied
    if not request.user.is_superuser:
        ras = request.user.profile.registrarAuthorities
        wgs = MDR.Workgroup.objects.filter(registrationAuthorities__in=ras)
        items = MDR._concept.objects.filter(workgroup__in=wgs)
    else:
        items = MDR._concept.objects.all()
    items = items.filter(readyToReview=True,statuses=None)
    page = render(request,"aristotle_mdr/user/userReadyForReview.html",{'items':items})
    return page

@login_required
def userWorkgroups(request):
    page = render(request,"aristotle_mdr/user/userWorkgroups.html")
    return page

@login_required
def toggleFavourite(request, item_id):
    request.user.profile.toggleFavourite(item_id)
    return redirect('/item/%s' % item_id)

def registrationauthority(request, iid):
    return render_if_user_can_view(MDR.RegistrationAuthority,request,iid)
def allRegistrationAuthorities(request):
    ras = MDR.RegistrationAuthority.objects.order_by('name')
    return render(request,"aristotle_mdr/allRegistrationAuthorities.html",
        {'registrationAuthorities':ras}
        )

def glossary(request):
    pass
    return render(request,"aristotle_mdr/unmanaged/glossary.html",)
def glossaryAjaxlist(request):
    import json
    results = [g.json_link_list() for g in MDR.GlossaryItem.objects.all()] #visible(request.user).all()]
    return HttpResponse(json.dumps(results), content_type="application/json")

def glossaryById(request,iid):
    term = get_object_or_404(MDR.GlossaryItem,id=iid)
    return render(request,"aristotle_mdr/unmanaged/glossaryItem.html",{'item':term})
#def glossaryBySlug(request,slug):
#    term = get_object_or_404(MDR.GlossaryItem,id=iid)
#    return render(request,"aristotle_mdr/glossaryItem.html",{'item':term})

def aboutThisSite(request):
    return render(request,"aristotle_mdr/about_this_site.html")

def aboutExtensions(request):
    return render(request,"aristotle_mdr/extensions.html",{'extensions':extensions})

# creation tools

def createProperty(request):
    return createManagedObject(request,MDRForms.PropertyForm)

def createObjectclass(request):
    return createManagedObject(request,MDRForms.ObjectClassForm)

def createValueDomain(request):
    return createManagedObject(request,MDRForms.ValueDomainForm)

def createDataElementConcept(request):
    return createManagedObject(request,MDRForms.DataElementConceptForm)

def createManagedObject(request,f):
    if request.user.is_anonymous():
        return redirect('/accounts/login?next=%s' % request.path)
    similar = None # We keep track of any similar items to prompt users to reuse
    prompt = False # Has the user tried to pass through again after being told to check other items?
    initial = {'workgroup':request.user.profile.activeWorkgroup,
         #'name':request.user.username
         }
    # What does the user want to clone? Technically this is the 'source' and we make the clone, but lets be pragmatic, not pedantic.
    clone = request.GET.get('clone',None)
    if clone is not None:
        clone = get_object_or_404(f.Meta.model,id=clone)
    supersede = request.GET.get('supersede',None)
    if supersede is not None:
        supersede = get_object_or_404(f.Meta.model,id=supersede)
    user = request.user
    frm = lambda *args, **kwargs: f(user=user,*args,**kwargs)
    if request.method == 'POST': # If the form has been submitted...
        form = frm(request.POST) # A form bound to the POST data
        initial = form
        if form.is_valid():
            errorWaived = form.data.get('userSwearsTheyKnowWhatTheyAreDoing','off') == 'on'

            similar = [None]
            if not errorWaived and clone is None:
                # Only search the database for similar items if the user hasn't waived the warning
                similar = f.Meta.model.objects.filter(
                        name__icontains=form.cleaned_data['name']
                    )

                similar = [o for o in similar if o.is_public]
                similarName = SearchQuerySet().models(f.Meta.model).filter(name=form.cleaned_data['name'])
                similarDesc = SearchQuerySet().models(f.Meta.model).filter(content=form.cleaned_data['description'])
                similarSyns = SearchQuerySet().models(f.Meta.model).filter(content=form.cleaned_data['synonyms'])
                similar = SearchQuerySet().models(f.Meta.model).filter_or(
                        name=form.cleaned_data['name'],
                        content=form.cleaned_data['description']+" "+form.cleaned_data['synonyms']) #.filter(states="Standard")
                print "----------------\n\n"
                print similar,form.cleaned_data['synonyms']
                print "\n\n"
                print SearchQuerySet().spelling_suggestion(form.cleaned_data['name'])
                print "\n\n----------------"

            if errorWaived or len(similar) == 0:

                newObj = f.Meta.model(**form.cleaned_data)
                newObj.save()
                supersede = request.GET.get('supersede',None)
                if supersede is not None:
                    s = f.Meta.model.objects.get(id=int(supersede))
                    # Add the realtionship on the superseder in case we change from one-to-many to many-to-many.
                    newObj.supersedes.add(s)
                newObj.save()
                messages.success(request,
                        _("New %(name)s Saved")%{'name':form.cleaned_data['name']}
                )
                return HttpResponseRedirect('/item/%d'% newObj.pk) # Redirect after POST
            else:
                prompt = True
    else:
        if clone is not None:
            # We want to clone an item, so find it and use that as the instance.
            form = frm( instance = clone,initial=initial ) # An unbound form
        elif supersede is not None:
            # We want to supersede an item, so find it and use that as the instance.
            form = frm( instance = supersede,initial=initial ) # An unbound form
        else:
            # We just want to make a new item
            form = frm( initial = initial ) # An unbound form

    return render(request, f.template, {
        'form': form,
        'similarObjects': similar,
        'clone': clone,
        'prompt':['','prompt'][prompt],
    })


"""
    Looks for items ot a given item type with the given search terms
"""
def findSimilar(itemType,name="",description="",synonyms=""):
    similar = SearchQuerySet().models(itemType).filter_or(
            name=name,
            content=description+" "+synonyms) #.filter(states="Standard")
    return similar




# wizards

TEMPLATES = {
        "initial": "aristotle_mdr/create/dec_1_initial_search.html",
        "results": "aristotle_mdr/create/dec_2_search_results.html",
        }

class DataElementConceptWizard(SessionWizardView):
    template_name = "aristotle_mdr/create/dec_template_wrapper.html"
    form_list = [("initial", MDRForms.DEC_Initial_Search),
                  ("results", MDRForms.DEC_Results),
                 ]

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def process_step(self,form):
        if self.steps.current == 'initial':
            print form.cleaned_data['oc_name']
            self.search_terms = {
                'oc_name': form.cleaned_data['oc_name'],
                'oc_desc': form.cleaned_data['oc_desc'],
                'pr_name': form.cleaned_data['pr_name'],
                'pr_desc': form.cleaned_data['pr_desc'],
            }

    def get_form_kwargs(self, step):
        # determine the step if not given
        if step is None:
            step = self.steps.current

        if step == 'results':
            return { 'oc_results': findSimilar(MDR.ObjectClass,
                                self.search_terms['oc_name'],
                                self.search_terms['oc_desc']
                            ),
                     'pr_results': findSimilar(MDR.Property,
                                self.search_terms['pr_name'],
                                self.search_terms['pr_desc']
                            )}
        return {}

    def get_context_data(self, form, **kwargs):
        context = super(DataElementConceptWizard, self).get_context_data(form=form, **kwargs)
        return context
        if self.steps.current == 'initial':
            context.update({'test': "hello"})
        if self.steps.current == 'results':
            context.update({'oc_results': findSimilar(MDR.ObjectClass,
                                self.search_terms['oc_name'],
                                self.search_terms['oc_desc']
                            )})
            context.update({'pr_results': findSimilar(MDR.Property,
                                self.search_terms['pr_name'],
                                self.search_terms['pr_desc']
                            )})
        return context


    def done(self, form_list, **kwargs):
        pass

# Actions
def removeWorkgroupRole(request,iid,role,userid):
    workgroup = get_object_or_404(MDR.Workgroup,pk=iid)
    if not (workgroup and user_is_workgroup_manager(request.user,workgroup)):
        if request.user.is_anonymous():
            return redirect('/accounts/login?next=%s' % request.path)
        else:
            raise PermissionDenied
    try:
        user = User.objects.get(id=userid)
        workgroup.removeRoleFromUser(role,user)
    except:
        pass
    return HttpResponseRedirect('/workgroup/%s/members'%(workgroup.id))

def addWorkgroupMembers(request,iid):
    workgroup = get_object_or_404(MDR.Workgroup,pk=iid)
    if not (workgroup and user_is_workgroup_manager(request.user,workgroup)):
        if request.user.is_anonymous():
            return redirect('/accounts/login?next=%s' % request.path)
        else:
            raise PermissionDenied
    if request.method == 'POST': # If the form has been submitted...
        form = MDRForms.AddWorkgroupMembers(request.POST) # A form bound to the POST data
        if form.is_valid():
            # process the data in form.cleaned_data as required
            users = form.cleaned_data['users']
            roles = form.cleaned_data['roles']
            for user in users:
                for role in roles:
                    workgroup.giveRoleToUser(role,user)
            return HttpResponseRedirect('/workgroup/%s/members'%(workgroup.id))
    else:
        form = MDRForms.AddWorkgroupMembers(initial={'roles':request.GET.get('role')})


    return render(request,"aristotle_mdr/actions/addWorkgroupMember.html",
            {"item":workgroup,
             "form":form,
             "role":request.GET.get('role')
                }
            )
def changeStatus(request, iid):
    item = get_object_or_404(MDR._concept,pk=iid)
    item = MDR._concept.objects.get_subclass(pk=iid)
    if not (item and user_can_change_status(request.user,item)):
        if request.user.is_anonymous():
            return redirect('/accounts/login?next=%s' % request.path)
        else:
            raise PermissionDenied
    # There would be an else here, but both branches above return,
    # so we've chopped it out to prevent an arrow anti-pattern.
    ras=request.user.profile.registrarAuthorities
    if request.method == 'POST': # If the form has been submitted...
        form = MDRForms.ChangeStatusForm(request.POST,ras=ras) # A form bound to the POST data
        if form.is_valid():
            # process the data in form.cleaned_data as required
            ras = form.cleaned_data['registrationAuthorities']
            state = form.cleaned_data['state']
            regDate = form.cleaned_data['registrationDate']
            cascade = form.cleaned_data['cascadeRegistration']
            if regDate is None:
                regDate = timezone.now().date()
            for ra in ras:
                ra = MDR.RegistrationAuthority.objects.get(id=int(ra))
                ra.register(item,state,request.user,regDate,cascade)
            return HttpResponseRedirect(reverse("aristotle:%s"%item.url_name(),args=[item.id]))
    else:
        form = MDRForms.ChangeStatusForm(ras=ras)
    return render(request,"aristotle_mdr/actions/changeStatus.html",
            {"item":item,
             "form":form,
                }
            )

def supersede(request, iid):
    item = get_object_or_404(MDR._concept,pk=iid).item
    if not (item and user_can_edit(request.user,item)):
        if request.user.is_anonymous():
            return redirect('/accounts/login?next=%s' % request.path)
        else:
            raise PermissionDenied
    qs=item.__class__.objects.all()
    if request.method == 'POST': # If the form has been submitted...
        form = MDRForms.SupersedeForm(request.POST,user=request.user,item=item,qs=qs) # A form bound to the POST data
        if form.is_valid():
            item.superseded_by = form.cleaned_data['newerItem']
            item.save()
            return HttpResponseRedirect(reverse("aristotle:item",args=[item.id]))
    else:
        form = MDRForms.SupersedeForm(item=item,user=request.user,qs=qs)
    return render(request,"aristotle_mdr/actions/supersedeItem.html",
            {"item":item,
             "form":form,
                }
            )

def deprecate(request, iid):
    item = get_object_or_404(MDR._concept,pk=iid).item
    if not (item and user_can_edit(request.user,item)):
        if request.user.is_anonymous():
            return redirect('/accounts/login?next=%s' % request.path)
        else:
            raise PermissionDenied
    qs=item.__class__.objects.filter().editable_slow(request.user)
    if request.method == 'POST': # If the form has been submitted...
        form = MDRForms.DeprecateForm(request.POST,user=request.user,item=item,qs=qs) # A form bound to the POST data
        if form.is_valid():
            # Check use the itemset as there are permissions issues and we want to remove some:
            #  Everything that was superseded, but isn't in the returned set
            #  Everything that was in the returned set, but isn't already superseded
            #  Everything left over can stay the same, as its already superseded
            #    or wasn't superseded and is staying that way.
            for i in item.supersedes.all():
                if i not in form.cleaned_data['olderItems'] and user_can_edit(request.user,i):
                    item.supersedes.remove(i)
            for i in form.cleaned_data['olderItems']:
                if user_can_edit(request.user,i): #Would check item.supersedes but its a set
                    item.supersedes.add(i)
            return HttpResponseRedirect(reverse("aristotle:item",args=[str(item.id)]))
    else:
        form = MDRForms.DeprecateForm(user=request.user,item=item,qs=qs)
    return render(request,"aristotle_mdr/actions/deprecateItems.html",
            {"item":item,
             "form":form,
                }
            )

def browse(request,oc_id=None,dec_id=None):
    if oc_id is None:
        items = MDR.ObjectClass.objects.order_by("name").public()
        return render(request,"aristotle_mdr/browse/objectClasses.html",
            {"items":items,
                }
            )
    elif oc_id is not None and dec_id is None:
        oc = get_object_or_404(MDR.ObjectClass,id=oc_id)
        items = MDR.DataElementConcept.objects.filter(objectClass=oc).order_by("name").public()
        return render(request,"aristotle_mdr/browse/dataElementConcepts.html",
            {"items":items,
             "objectClass":oc,
                }
            )
    elif oc_id is not None and dec_id is not None:
        # Yes, for now we ignore the Object Class. If the user is messing with IDs in the URL and things break thats their fault.
        dec = get_object_or_404(MDR.DataElementConcept,id=dec_id)
        items = MDR.DataElement.objects.filter(dataElementConcept=dec).order_by("name").public()
        return render(request,"aristotle_mdr/browse/dataElements.html",
            {"items":items,
             "dataElementConcept":dec,
                }
            )

def bulkFavourite(request,url="aristotle:userFavourites"):
    print request.GET.getlist('favourites',[])
    for item in request.GET.getlist('favourites',[]):
        item = get_or_none(MDR.trebleObject,id=int(item))
        if item and user_can_view(request.user,item):
            request.user.profile.favourites.add(item)
    getVars = request.GET.copy()
    if 'favourites' in getVars.keys(): getVars.pop('favourites')
    if 'addFavourites' in getVars.keys(): getVars.pop('addFavourites')
    return HttpResponseRedirect(reverse(url)+'?'+urllib.urlencode(getVars))

# Search views

class PermissionSearchView(SearchView):
    def __call__(self, request):
        if 'addFavourites' in request.GET.keys():
            return bulkFavourite(request,url="aristotle:search")
        else:
            return super(PermissionSearchView, self).__call__(request)

    def build_form(self):
        form = super(self.__class__, self).build_form()
        form.request = self.request
        return form

