from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Polygon
from django.contrib.gis.geos import Point
import csv

from ceom.photos.models import Photo, Category
from ceom.maps.models import GeocatterPoint
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.paginator import Paginator



def index(request):
    return render(request, 'maps/index.html')


@login_required
def geocatter(request):
    data = {}
    data['category_list'] = Category.objects.all()

    if request.method == 'POST':
        print(request.POST)

        # Small pixel
        GeocatterPoint.objects.create(
            user = request.user,
            date_taken = request.POST['date'],
            grid_npix = request.POST['s-npix'],
            tile_h = request.POST['s-tileh'],
            tile_v = request.POST['s-tilev'],
            pixel_x = request.POST['s-pixelx'],
            pixel_y = request.POST['s-pixely'],
            center = Point(float(request.POST['s-centerx']), float(request.POST['s-centery'])),
            is_multi_cat = 's-multicat' in request.POST,
            primary_category = Category.objects.get(name=request.POST['s-cat1-select']),
            secondary_category = Category.objects.get(name=request.POST['s-cat2-select']) if 's-multicat' in request.POST else None,
        )

        # Medium pixel
        GeocatterPoint.objects.create(
            user = request.user,
            date_taken = request.POST['date'],
            grid_npix = request.POST['m-npix'],
            tile_h = request.POST['m-tileh'],
            tile_v = request.POST['m-tilev'],
            pixel_x = request.POST['m-pixelx'],
            pixel_y = request.POST['m-pixely'],
            center = Point(float(request.POST['m-centerx']), float(request.POST['m-centery'])),
            is_multi_cat = 'm-multicat' in request.POST,
            primary_category = Category.objects.get(name=request.POST['m-cat1-select']),
            secondary_category = Category.objects.get(name=request.POST['m-cat2-select']) if 'm-multicat' in request.POST else None,
        )

        # Large pixel
        GeocatterPoint.objects.create(
            user = request.user,
            date_taken = request.POST['date'],
            grid_npix = request.POST['l-npix'],
            tile_h = request.POST['l-tileh'],
            tile_v = request.POST['l-tilev'],
            pixel_x = request.POST['l-pixelx'],
            pixel_y = request.POST['l-pixely'],
            center = Point(float(request.POST['l-centerx']), float(request.POST['l-centery'])),
            is_multi_cat = 'l-multicat' in request.POST,
            primary_category = Category.objects.get(name=request.POST['l-cat1-select']),
            secondary_category = Category.objects.get(name=request.POST['l-cat2-select']) if 'l-multicat' in request.POST else None,
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

def leaderboard(request):
    data = {}
    ranks = User.objects.annotate(points=Count('geocatterpoint')).order_by("-points")
    paginator = Paginator(ranks, 25) 
    page_number = request.GET.get('page')
    data['page_obj'] = paginator.get_page(page_number)
    return render(request, 'maps/leaderboard.html', context=data)

def pixels_validation(request):
    return render(request, 'maps/pixels_validation.html')

def pixels_validation_csv(request):
    poly = Polygon.from_bbox((request.GET['xmin'], request.GET['ymin'], request.GET['xmax'], request.GET['ymax']))
    
    geocatterPoints = GeocatterPoint.objects.filter(center__within=poly)

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)

    #Header
    writer.writerow(['Tile h', 'Tile v', 'Grid npix', 'Pixel x', 'Pixel y', 'Multiple Categories', 'Primary Category', 'Secondary Category', 'Date categorized'])

    for p in geocatterPoints:
        writer.writerow([p.tile_h, p.tile_v, p.grid_npix, p.pixel_x, p.pixel_y, p.is_multi_cat, p.primary_category, p.secondary_category, p.date_categorized])

    return response
