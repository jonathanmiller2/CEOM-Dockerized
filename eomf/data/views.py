from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
import os, mapnik
from copy import deepcopy
from ogcserver.WMS import BaseWMSFactory
from util import *

base_path, tail = os.path.split(__file__)

modis_srs = "+proj=sinu +R=6371007.181 +nadgrids=@null +wktext"
modis_srs = "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"
merc_srs  = "+init=epsg:3857"
stand_srs = "+init=epsg:4326"

def getModisScale(prod):
    params = {'evi'  : [[250,250,150],[130,10,10]  ,[0,140,0]    ,0.3,-0.20,1, None, 0.1],
              'ndsi' : [[255,250,250],[130,0,0]    ,[140,140,140],0  ,-0.6 ,1, None, 0.1],
              'ndvi' : [[250,250,150],[130,10,10]  ,[0,140,0]    ,0.3,-0.20,1, None, 0.1],
              'ndwi' : [[250,250,250],[130,130,130],[0,140,0]    ,0  ,-0.4 ,1, None, 0.1],
              'lswi' : [[250,250,250],[190,46,6]   ,[3,156,21]   ,0  ,-0.4 ,1, None, 0.1]}
    
    return makeThreeScale(*params[prod])

def getEcohealthScale(name):
    if name == "ccode":
        return  [{'color':[242,242,242],'stop':6},
                {'color':[244,188,169],'stop':7},
                {'color':[240,177,95], 'stop':8},
                {'color':[231,207,2],  'stop':9},
                {'color':[281,230,0],  'stop':10},
                {'color':[87,214,16],  'stop':11},
                {'color':[0,176,20 ],  'stop':12},
                {'color':[0,100,0  ],  'stop':13}]
    
    params = {'chdn'  : [[231,207,2],[242,242,242],[0,176,20 ] ,4000,0,6000, 16, None, True],
              'dudn'  : [[231,207,2],[242,242,242],[0,176,20 ] ,2000,0,4000, 16, None],
              'hpdn'  : [[251,220,2],[25,196,40 ], [217,0,0 ]  ,1000,0,6500, 16, None, True],
              'dem'   : [[231,207,2],[242,242,242],[0,176,20 ] ,5000,0,7000, 16, None],
              'ncropn': [[231,207,2],[242,242,242],[0,176,20 ] ,1   ,0,2   , 16, None],
              'ncropo': [[231,207,2],[242,242,242],[0,176,20 ] ,1.5 ,0,3   , 16, None],
              'pnaspred':[[231,207,2],[242,242,242],[0,176,20] ,0.5 ,0,1   , 16, None],
              'sapred': [[231,207,2],[242,242,242],[0,176,20 ] ,0.5 ,0,1   , 16, None]}
    
    return makeThreeScale(*params[name])

##########VIEWS###########

def wms(request):

    datas = [{'name': 'chdn',    'long_name': 'Chicken density'},
             {'name': 'dudn',    'long_name': 'Duck density'},
             {'name': 'hpdn',    'long_name': 'Human Population'},
             {'name': 'dem',     'long_name': 'Elevation'},
             {'name': 'ncropn',  'long_name': 'Cropping intensity (new methid)'},
             {'name': 'ncropo',  'long_name': 'Cropping intensity (PNAS version)'},
             {'name': 'pnaspred','long_name': 'PNAS model predictions'},
             {'name': 'sapred',  'long_name': 'South Asia Model Predictions'},
             {'name': 'ccode',   'long_name': 'Country Code(categorical)'}]
                 
    class WMSFactory(BaseWMSFactory):
        def __init__(self):
            BaseWMSFactory.__init__(self)
            for data in datas:
                name = data['name']
                title = data['long_name']      
                data = base_path+"/ecohealth/"+name+'.asc'
                
                layer = mapnik.Layer(name,"+init=epsg:4326")
                layer.datasource = mapnik.Gdal(file=str(data),band=1) 
                layer.title = title
                layer.queryable = True
                layer.wms_srs = None
                style = mapnik.Style()
                rule = mapnik.Rule()
                sym = mapnik.RasterSymbolizer()
                sym.colorizer = mapnik.RasterColorizer(mapnik.COLORIZER_LINEAR, mapnik.Color("transparent"))
                scale = getEcohealthScale(name)
                for color in scale:
                    sym.colorizer.add_stop(color['stop'], mapnik.Color(*color['color']))
                rule.symbols.append(sym)
                style.rules.append(rule)

                self.register_style(name,style)
                self.register_layer(layer, name, (name,))
            self.finalize()

    return ogc_response(request, WMSFactory())

def modis_wms(request, product='evi'):
    year = int(request.GET['year'])
    day =  int(request.GET['day'])
    if year <= 2005:
        path = "/data/vol02/modis/products/mod09a1/geotiff"
    else:
        path = "/data/vol05/modis/products/mod09a1/geotiff"
        
    data = "%s/%s/%d/globe/%s_%d%03d_10km_mosaic.tif" % ( path, product, year, product, year, day)

    class WMSFactory(BaseWMSFactory):
        def __init__(self):
            BaseWMSFactory.__init__(self)

            layer = mapnik.Layer('TOP', modis_srs)
            layer.datasource = mapnik.Gdal(file=str(data),band=1) 
            layer.title = "Modis VI Layer"
            layer.queryable = True
            layer.wms_srs = None
            style = mapnik.Style()
            rule = mapnik.Rule()
            sym = mapnik.RasterSymbolizer()
            sym.colorizer = mapnik.RasterColorizer(mapnik.COLORIZER_DISCRETE, mapnik.Color("transparent"))
            scale = getModisScale(product)
            for color in scale:
                sym.colorizer.add_stop(color['stop'], mapnik.Color(*color['color']))
            rule.symbols.append(sym)
            style.rules.append(rule)
            self.register_style('modis_style', style)
            self.register_layer(layer, "modis_style",("modis_style",))

            layer = mapnik.Layer('ocean_mask')
            layer.datasource = mapnik.Shapefile(file=str("/data/health/data1/web/data/shapes/50m_ocean.shp"))
            layer.queryable = True
            layer.wms_srs = None
            style = mapnik.Style()
            rule = mapnik.Rule()
            poly_sym = mapnik.PolygonSymbolizer(mapnik.Color('#50649B'))
            rule.symbols.append(poly_sym)
            style.rules.append(rule)
            self.register_style('mask_style', style)
            self.register_layer(layer, "mask_style",("mask_style",))
    
    mapfactory = WMSFactory()
    return ogc_response(request, mapfactory)

def photos(request):                
    class WMSFactory(BaseWMSFactory):
        def __init__(self):
            BaseWMSFactory.__init__(self)
            name = "photos"
            title = "Geo-tagged photos"      
            
            select = "photos"
            select = '''(SELECT kmeans, count(*), ST_Centroid(ST_Collect(point)) AS point 
                        FROM (
                          SELECT kmeans(ARRAY[ST_X(point), ST_Y(point)], 100) OVER (), point
                          FROM photos WHERE point is not NULL
                        ) AS ksub
                        GROUP BY kmeans
                        ORDER BY kmeans) as result '''

            select = '''(SELECT kmeans, count(*), ST_ConvexHull(ST_Collect(point)) AS point 
                        FROM (
                          SELECT kmeans(ARRAY[ST_X(point), ST_Y(point)], 100) OVER (), point
                          FROM photos WHERE point is not NULL
                        ) AS ksub
                        GROUP BY kmeans
                        ORDER BY kmeans) as result '''
                        
            layer = mapnik.Layer(name,"+init=epsg:4326")
            layer.datasource = mapnik.PostGIS(host='localhost',
                                              user='rsadmin',
                                              password='b1u3b1rd',
                                              dbname='remotesensing',
                                              table=select)
            layer.title = title
            layer.queryable = True
            layer.wms_srs = None
            style = mapnik.Style()
            rule = mapnik.Rule()
            #icon = "/web/eomf/dev/eomf/photos/circle.svg"
            sym = mapnik.PointSymbolizer()
            sym2 = mapnik.PolygonSymbolizer()
            #sym.filename = "/web/eomf/dev/eomf/photos/circle.svg"
            sym.allow_overlap = True
            sym.opacity = .5
            rule.symbols.append(sym)
            rule.symbols.append(sym2)
            style.rules.append(rule)

            self.register_style(name,style)
            self.register_layer(layer, name, (name,))
            self.finalize()

    return ogc_response(request, WMSFactory())


# its easy to do per user permissions:
#
# if not request.user.has_perm(app.model):
#    raise Http404
#
# or globally protect map services to authenticated users
# @login_required
# def tile_serving_view(request):

