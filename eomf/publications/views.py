from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from eomf.publications.models import Publication, Category


def index(request):
    pubs = Publication.objects.all().order_by('date')
    #pubs.reverse()

    if 'type' in request.GET:
        pubs = pubs.filter(pubtype=str(request.GET['type']))

    years = dict()
    for pub in pubs:
        if pub.year:
            year = pub.year
        else:
            year = pub.date.year

        year_list = years.get(year, [])
        year_list.append(pub)
        years[year] = year_list

    return render_to_response(
        'publications/section_list.html',
        {
            'section_list': years
        },
        context_instance=RequestContext(request)
    )


def detail(request):
    '''
    This can be a future view to display a single publication with content
    '''

    return HttpRequest()
