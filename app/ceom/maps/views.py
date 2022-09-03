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
            date_taken = request.POST['date'],
            category = Category.objects.get(name=request.POST['category'])
        )
        return HttpResponse()
    return render(request, 'maps/geocatter.html', context=data)

def map_validation(request):
    return render(request, 'maps/map_validation.html')

def map_validation_data(request):
    box = Polygon.from_bbox((request.GET['l'], request.GET['d'], request.GET['r'], request.GET['u']))
    
    unclassified_category = Category.objects.get(name__iexact="Unclassified")
    photos = Photo.objects.filter(point__isnull=False, point__bboverlaps=box).exclude(category_id=unclassified_category).exclude(category_id__isnull=True).exclude(takendate__isnull=True)

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)

    #Header
    writer.writerow(['lat', 'lon', 'category_id', 'category_name', 'date_taken'])

    for photo in photos:
        writer.writerow([photo.point.y, photo.point.x, photo.category.id, photo.category.name, photo.takendate])

    return response