from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Polygon, Point

import csv
import json

from ceom.photos.models import Photo, Category, CategoryVote
from ceom.maps.models import GeocatterPoint
from django.contrib.auth.models import User
from django.db.models import Count, Sum, When, Case, Q 
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

@login_required
def geocatterphoto(request, photo_id=None):
    unclassified_category = Category.objects.get(name__iexact='Unclassified')
    users_voted_photos = CategoryVote.objects.filter(user=request.user).values_list('photo')
    photo_set = Photo.objects.filter(point__isnull=False).filter(Q(category__isnull=True) | Q(category=unclassified_category)).filter(status=1).exclude(id__in=users_voted_photos).order_by('?')[:1]
    photoid = photo_set[0].id

    if photo_id is None or photo_id == '':
        photo_id = str(photoid)
        return redirect(f'/maps/geocatterphoto/{photo_id}/')
    
    if photo_id != str(photoid):
        photo_id = photoid
        photo_url = f'/maps/geocatterphoto/{photo_id}/'

        # Check if the current URL already contains the correct photo_id
        current_url = request.get_full_path()
        if f'/maps/geocatterphoto/{photo_id}/' in current_url:
            print("Already redirected to the correct photo_id. Skipping redirection.")
        else:
            if 'redirected' not in request.session:
                print("redirected")
                request.session['redirected'] = True
                return redirect(photo_url)
    
    data = {}

    user_vote_count = len(users_voted_photos)
    lat_list = [photo.point.y for photo in photo_set]
    lon_list = [photo.point.x for photo in photo_set]
    dates = [photo.takendate for photo in photo_set]

    #If there are no photos that are geolocated, unclassified, and public
    if photo_set.count() <= 0:
        #Then just show a photo that is geolocated, classified, and public
        photo_set = Photo.objects.filter(point__isnull=False).filter(status=1).exclude(id__in=users_voted_photos).order_by('?')[:1]
    #If there are still no photos
    if photo_set.count() <= 0:
        print("No photos")
        return render(request, 'maps/geocatterphoto.html')

    data['lat'] = lat_list[0]
    data['lon'] = lon_list[0]
    data['score'] = user_vote_count
    data['photo'] = photo_set[0]
    data['photo_url'] = f'/maps/geocatterphoto/{photo_id}/'
    data['date'] = dates[0]
    data['landcover_categories'] = Category.objects.all()
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
        new_photo_set = Photo.objects.filter(point__isnull=False).filter(Q(category__isnull=True) | Q(category=unclassified_category)).filter(status=1).exclude(id__in=users_voted_photos).order_by('?')[:1]
        new_photo_id = new_photo_set[0].id
        data['photo_url'] = f'/maps/geocatterphoto/{new_photo_id}/'
        print(new_photo_id)
        print(f'/maps/geocatterphoto/{new_photo_id}/')
        response_data = {'new_photo_id': new_photo_id}
        return JsonResponse(response_data)
    
    return render(request, 'maps/geocatterphoto.html', context=data)

def point_validation(request):
    return render(request, 'maps/point_validation.html')

def point_validation_csv(request):
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

def pixel_validation(request):
    data = {}
    centers = GeocatterPoint.objects.values('center', 'grid_npix')
    centers_list = [(center['center'].x, center['center'].y, center['grid_npix']) for center in centers]
    data = {'centers_list': json.dumps(centers_list)}
    return render(request, 'maps/pixel_validation.html', context=data)


def pixel_validation_csv(request):
    poly = Polygon.from_bbox((request.GET['xmin'], request.GET['ymin'], request.GET['xmax'], request.GET['ymax']))
    
    geocatterPoints = GeocatterPoint.objects.filter(center__within=poly)

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)

    #Header
    writer.writerow(['Grid_size', 'Grid_npix', 'Tile_H', 'Tile_V', 'Pixel_X', 'Pixel_Y', 'Date_Categorized', 'Multiple_Categories', 'Primary_Category', 'Secondary_Category'])

    for p in geocatterPoints:
        writer.writerow([int((1200/p.grid_npix)*1000), p.grid_npix, p.tile_h, p.tile_v, p.pixel_x, p.pixel_y, p.date_categorized, p.is_multi_cat, p.primary_category, p.secondary_category])

    return response
