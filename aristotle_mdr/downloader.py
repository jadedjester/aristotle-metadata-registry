#aristotle_ddi_utils
from aristotle_mdr.utils import get_download_template_path_for_item
import cgi
import cStringIO as StringIO
from django.http import HttpResponse, Http404
#from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
import xhtml2pdf.pisa as pisa

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result,encoding='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))

def download(request,downloadType,item):
    template = get_download_template_path_for_item(item,downloadType)

    from django.conf import settings
    page_size = getattr(settings, 'PDF_PAGE_SIZE', "A4")

    if downloadType=="pdf":
        subItems = item.getPdfItems
        return render_to_pdf(template,
            {'item':item,
             'items':subItems,
             'tableOfContents':len(subItems)>0,
             'view':request.GET.get('view','').lower(),
             'pagesize':request.GET.get('pagesize',page_size),
            }
        )

    raise Http404