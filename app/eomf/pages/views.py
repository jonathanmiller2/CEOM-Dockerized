from eomf.pages.models import ContentPage
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.utils.safestring import mark_safe

from django.shortcuts import render_to_response

DEFAULT_TEMPLATE = 'pages/default.html'

def contentpage(request, url):
    """
    Flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or `flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """

    

    if not url== '' and not url.endswith('/') and settings.APPEND_SLASH:
        print("DEBUG*** 27 ***DEBUG")
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        print("DEBUG*** 30 ***DEBUG")
        url = "/" + url
    
    print("DEBUG*** 33 ***DEBUG")
    print("url:", url)
    print("sites_id:", settings.SITE_ID)
    try:
        #If 
        f = get_object_or_404(ContentPage, url__exact=url)#, sites__id__exact=settings.SITE_ID)
    except Exception as e:
        print("*DEBUG*** 38 *** DEBUG " + str(e))
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.

    print("DEBUG*** 39 ***DEBUG")

    if f.registration_required and not request.user.is_authenticated():
        print("DEBUG*** 41 ***DEBUG")
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    #if f.template_name:
    #    t = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    #else:
    #    t = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)
    try:
        print("DEBUG*** 52 ***DEBUG")
        return render_to_response(f.template_name, {'flatpage':f})
        #return render(request, f.template_name, {'flatpage': f})
    except:
        print("DEBUG*** 58 ***DEBUG")
        return render_to_response(f.template_name, {'flatpage':f})
   # response = HttpResponse(t.render(c))
    #try:
    #    from django.core.xheaders import populate_xheaders
    #    populate_xheaders(request, response, ContentPage, f.id)
    #except ImportError:
    #    pass
   # return response
    print("DEBUG*** end ***DEBUG")