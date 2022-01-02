from ceom.modis.inventory.models import File, Product, Dataset, Tile
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import numpy
import sys, os

def remote_sensing_datasets(request):
    # existing = File.objects.values('dataset').distinct()
    # dataset_list = Dataset.objects.filter(file__dataset_id__isnull=False).order_by("name")
    dataset_list = Dataset.objects.all().order_by("name")
    product_list = Product.objects.all().order_by("name")

    return render(request, 'inventory/remote_sensing_datasets.html', context={
        'dataset_list' : dataset_list,
        'product_list' : product_list,
    })

def tilemap(request, dataset_id, year):
    dataset = Dataset.objects.get(name__iexact=dataset_id)

    # Need to replace existing and dataset_list query. It is too slow... use subqueries and group by!!!  
    existing = File.objects.distinct().values('dataset')
    #existing = [mcd43a4,mod09a1,mod09ga,mod09q1,mod11a1,mod11a2,mod11c3,mod12q1,mod13a1,mod13a2,mod13c2,mod13q1,mod14a2,mod15a2,mod17a2,myd11a2,myd11c3,myd14a2]
    dataset_list = Dataset.objects.filter(name__in=existing)
    # dataset_list contains all the information of the product in the existing list above
    year_list = File.objects.filter(dataset=dataset).distinct().order_by('year').values('year')
    #year_list = [2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016]

    good_list = []
    bad_list = []

    def splittiles(n):
        for tile in Tile.objects.with_count(dataset_id,year):
            if tile.count == n:
                good_list.append(tile)
            else:
                bad_list.append(tile)
    
    if year == '2000':
        splittiles(40)
    elif year == '2001':
        splittiles(45)
    else:
        splittiles(46)

    return render(request, 'inventory/map.html', context={
        'dataset' : dataset_id,
        'dataset_list' : dataset_list,
        'good_list' : good_list,
        'bad_list' : bad_list,
        'year' : year,
        'year_int': int(year),
        'year_list' : year_list,
    })
    
def tile(request, x, y):

    #TODO: Why are there two files named the same thing?
    def daystoranges( days,day_res):
        l = []
        if len(days) > 0:
            rang = []
            rang.append(days[0])
            prev = days[0]

            for i in range(1, len(days)):
                if days[i]-day_res != prev:
                    l.append(rang)
                    rang = []
                rang.append(days[i])
                prev = days[i]
            l.append(rang)
        for i in range(0,len(l)):
            l[i] = [l[i][0], l[i][-1]]
        return l

    def daysToRanges( days,day_res):
        ranges = []
        for r in daystoranges(days,day_res):
            if r[0] != r[1]:
                ranges.append('-'.join(map(str, r)))
            else:
                ranges.append(str(r[0]))

        return ', '.join(ranges)

    #This function takes sorted array of day numbers with 8 days
    # interval and returns the days that are missing
    def missingdays( days,day_res):
        l = []
        i = 0
        length = len(days)
        for d in range(1, 365, day_res):
            if (i>=length or d != days[i]):
                l.append(d)
            else:
                i=i+1

        return l

    def parsePresentMissing( days,day_res):
        s = daysToRanges(days,day_res)
        m = daysToRanges(missingdays(days,day_res),day_res)
        return s, m

    def getproducts(names,dataset_day_res_dict):
        dic = {}
        result = []
        for name in sorted(names):
            f = name.split('.')
            # MOD09A1.A2000185.h12v01.005.2006292063546.hdf
            if(f[5]=='hdf'):
                product = f[0]
                year = f[1][1:5]
                tile = f[2]
                day = f[1][-3:]
                dic.setdefault(product,{}).setdefault(year, {}).setdefault(tile,[]).append(int(day))

        # Could be improved by removing the expensive sorting by using lists ( O(log n))
        for p in sorted(dic.keys()):
            years = dic[p]
            year_list = []
            for y in sorted(years.keys()):
                tiles = years[y]
                tile_list = []
                for t in sorted(tiles.keys()):
                    days = tiles[t]
                    days.sort()
                    dataset_day_res_dict[p]
                    present, missing = parsePresentMissing(days,dataset_day_res_dict[p])
                    tile_list.append((t, {'ranges': present, 'missing': missing, 'total': len(days)}))
                year_list.append((y, tile_list))
            result.append((p, year_list))

        return result


    import datetime
    tileq = "h%02dv%02d" % (int(x),int(y))
    files_query = File.objects.filter(tile=tileq).values('name').order_by('name')
    dataset_day_res_query = Dataset.objects.all().values('name','day_res')
    dataset_day_res_dict = {d['name']:d['day_res'] for d in dataset_day_res_query}
    files = [ row['name'] for row in files_query]
    files = getproducts(files,dataset_day_res_dict)
    
    return render(request, 'inventory/tile.html', context={
        'tile': tileq,
        'files': files,
        'total': len(files_query),
    })
    
def tile_details(request, x, y):
    return HttpRequest()
    
def detail(request, product_id):
    try:
        prod = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404
    return render(request, 'inventory/remote_sensing_datasets.html', context={'prod': prod})


from PIL import Image
from django.conf import settings
from io import BytesIO

def toast_tile(request, z, x, y):
    RESULT_SIZE = 256, 256
    
    #print(z, x, y)
    with BytesIO() as output:
        with Image.open(os.path.join(settings.MEDIA_ROOT, "toast-image.png")) as im:
            width, height = im.size

            h_tilesize = width / (2 ** z)
            v_tilesize = height / (2 ** z)

            left = h_tilesize * x
            right = h_tilesize * (x + 1)
            top = v_tilesize * y
            bottom = v_tilesize * (y + 1)

            im = im.crop((left, top, right, bottom))
            if im.size[0] > RESULT_SIZE[0] or im.size[1] > RESULT_SIZE[1]:
                im.thumbnail(RESULT_SIZE, Image.ANTIALIAS)
            im.save(output, "png")
        return HttpResponse(output.getvalue(), content_type="image/png")
    
    