from eomf.pages.views import contentpage
from django.http import Http404
from django.conf import settings

#TODO: Check if this is used or needed whatsoever, I think it isn't
class ContentpageFallbackMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        #if self.get_response.status_code != 404:
        #    return self.get_response # No need to check for a flatpage for non-404 responses.
        #try:
        #    return contentpage(request, request.path_info)
        ## Return the original response if any errors happened. Because this
        ## is a middleware, we can't assume the errors will be caught elsewhere.
        #except Http404:
        #    return self.get_response
        #except:
        #    if settings.DEBUG:
        #        raise
        #    return self.get_response

        return self.get_response

