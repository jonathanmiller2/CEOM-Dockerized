from django.shortcuts import render
from ceom.photos.models import Category
from ceom.maps.models import GeocatterPoint


def index(request):
    return render(request, 'maps/index.html')


def geocatter(request):
    data = {}
    data['category_list'] = Category.objects.all()

    if request.method == 'POST' and 'category' in request.POST:
        GeocatterPoint.objects.create(
            lat = request.POST['lat'],
            lon = request.POST['lon'],
            category = Category.objects.get(name=request.POST['category'])
        )
        return HttpResponse()
    return render(request, 'maps/geocatter.html', context=data)
    