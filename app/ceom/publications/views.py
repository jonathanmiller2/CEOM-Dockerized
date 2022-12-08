from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import RequestContext
from ceom.aboutus.models import Publication, Category


def index(request):
    pubs = Publication.objects.all().order_by('-date')
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

    print(years)

    return render(request, 'publications/section_list.html', context={'section_list': years})

def detail(request):
    '''
    This can be a future view to display a single publication with content
    '''

    return HttpRequest()
