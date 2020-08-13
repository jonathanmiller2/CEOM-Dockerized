from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
import os, mapnik, numpy
from copy import deepcopy
from ogcserver.configparser import SafeConfigParser
from ogcserver.WMS import BaseWMSFactory
from ogcserver.wms111 import ServiceHandler as ServiceHandler111
from ogcserver.wms130 import ServiceHandler as ServiceHandler130
from ogcserver.exceptions import OGCException, ServerConfigurationError

base_path, tail = os.path.split(__file__)

#modis_srs = "+proj=sinu +R=6371007.181 +nadgrids=@null +wktext"
#modis_srs = "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"
modis_srs = "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
merc_srs  = "+init=epsg:3857"
stand_srs = "+init=epsg:4326"

from StringIO import StringIO
from mapnik import Image, render
from ogcserver.common import PIL_TYPE_MAPPING, Response

def newGetMap(self, params):
    # HACK: check if the image should be strechted
    bbox_ratio = float(params['bbox'][2] - params['bbox'][0]) / float(params['bbox'][3] - params['bbox'][1])
    image_ratio = float(params['width']) / float(params['height'])
    img_height = params['height']
    resize = False
    
    if int(bbox_ratio * 100) != int(image_ratio * 100):
        params['height'] = int(params['height'] / bbox_ratio)
        resize = True
    
    m = self._buildMap(params)
    im = Image(params['width'], params['height'])
    render(m, im)
    format = PIL_TYPE_MAPPING[params['format']]
    
    if resize:
        import Image as PILImage
        size = params['width'], params['height']
        im = PILImage.open(StringIO(im.tostring(format)))
        size = params['width'], img_height
        im = im.resize(size)
        output = StringIO()
        im.save(output, format=format)
        return Response(params['format'].replace('8',''), output.getvalue())
        
    return Response(params['format'].replace('8',''), im.tostring(format))

import ogcserver.common
patched = ogcserver.common.WMSBaseServiceHandler
patched.GetMap = newGetMap
ogcserver.common.WMSBaseServiceHandler = patched

def makeSimple(c1=[0,0,0],c2=[255,255,255], min=-1, max=1, num=16):
    op1 = '>='
    op2 = '<'
    val = min
    min, max = map(float, (min,max))
    scale = []
    while ( val < max ):
        val2 = val + (max-min)/num
        i = (val - min)/(max - min)
        if (val > min):
            op1 = '>'
        if (val2 == max):
            op2 = '<='
        name = "%01.2f - %01.2f" % (val, val2)
        exp = "([pixel] %s %f AND [pixel] %s %f)" % (op1, val, op2, val2)
        color = [c1[0]+(c2[0]-c1[0])*i, c1[1]+(c2[1]-c1[1])*i, c1[2]+(c2[2]-c1[2])*i ]
        scale.append({'name':name, 'exp':exp, 'color':color})
        val = val2
    return scale

def makeScale(colors, num=16):
    if len(colors)<2:
        return []
    else:
        scale = []
        prev_color = None
        prev_value = None
        values = sorted(colors.keys())
        bin_num = num / len(values)
        for value in values:
            if prev_value is not None:
                scale += makeSimple(prev_color,colors[value], prev_value, value, bin_num)
            prev_value = value
            prev_color = colors[value]

    return scale
    
def makeThreeScale(cm, c1, c2, mid, min=-1, max=1, num=16, step=None, log=False):
    if step is None:
        step = (max - min)/float(num)

    mid, min, max = map(float, (mid, min, max))
    scale = []
    i = 0
    mid1 = (mid - min)/step
    mid2 = (max - mid)/step
    val = min
    while ( val < max):
        val2 = val + step
        
        if (val == min):
            op1 = '>='
        else:
            op1 = '>'
            
        op2 = '<='
        name = "%01.2f - %01.2f" % (val, val2)
        exp = "([pixel] %s %f AND [pixel] %s %f)" % (op1, val, op2, val2)
        if (val2 < mid):
            color = [c1[0]+(cm[0]-c1[0])*(i/mid1), c1[1]+(cm[1]-c1[1])*(i/mid1), c1[2]+(cm[2]-c1[2])*(i/mid1) ]
        elif ((val <= mid) and (val2 >= mid)):
            color = cm
            i = 0
        elif (val > mid):
            color = [cm[0]+(c2[0]-cm[0])*(i/mid2), cm[1]+(c2[1]-cm[1])*(i/mid2), cm[2]+(c2[2]-cm[2])*(i/mid2) ]
        color = map(int, color)
        scale.append({'name':name, 'exp':exp, 'color':color, 'stop':val2})

        i += 1
        val = val2
    return scale

def makeThreeScale2(cm, c1, c2, mid, min=-1, max=1, num=16, step=None, log=False):
    mid, min, max, num = map(float, (mid, min, max, num))
    
    scale = []
    
    if log:
        values = numpy.logspace(min, max, num)
    else:
        values, step = numpy.linspace(min, max, num)
        #mid1 = (mid - min)/step
        #mid2 = (max - mid)/step
    
    i = 0
    for val in values:
        if i+1 > len(values):
            val2 = max
        else:
            val2 = values[i+1]
        
        if (val == min):
            op1 = '>='
        else:
            op1 = '>'
            
        op2 = '<='
        name = "%01.2f - %01.2f" % (val, val2)
        exp = "([pixel] %s %f AND [pixel] %s %f)" % (op1, val, op2, val2)
        if (val2 < mid):
            ratio1 = i / num / 2
            r = c1[0]+(cm[0]-c1[0]) * ratio1
            g = c1[1]+(cm[1]-c1[1]) * ratio1
            b = c1[2]+(cm[2]-c1[2]) * ratio1
            color = [r, g, b]
        elif ((val <= mid) and (val2 >= mid)):
            color = cm
            i = 0
        elif (val > mid):
            ratio1 = i / num / 2
            r = cm[0]+(c2[0]-cm[0]) * ratio2
            g = cm[1]+(c2[1]-cm[1]) * ratio2
            b = cm[2]+(c2[2]-cm[2]) * ratio2
            color = [r, g, b]
        
        color = map(int, color)
        
        scale.append({'name':name, 'exp':exp, 'color':color, 'stop':val2})

        i += 1
    return scale
    
def ogc_response(request, mapfactory):
    
    conf = SafeConfigParser()
    conf.readfp(open(base_path+"/ogcserver.conf"))
    
    reqparams = lowerparams(request.GET)
    if 'srs' in reqparams:
        reqparams['srs'] = str(reqparams['srs'])
    if 'styles' not in reqparams:
        reqparams['styles'] = ''

    onlineresource = 'http://%s%s?' % (request.META['HTTP_HOST'], request.META['PATH_INFO'])

    if not reqparams.has_key('request'):
        raise OGCException('Missing request parameter.')
    req = reqparams['request']
    del reqparams['request']
    if req == 'GetCapabilities' and not reqparams.has_key('service'):
        raise OGCException('Missing service parameter.')
    if req in ['GetMap', 'GetFeatureInfo']:
        service = 'WMS'
    else:
        service = reqparams['service']
    if reqparams.has_key('service'):
        del reqparams['service']
    try:
        ogcserver = __import__('ogcserver.' + service)
    except:
        raise OGCException('Unsupported service "%s".' % service)
    ServiceHandlerFactory = getattr(ogcserver, service).ServiceHandlerFactory
    servicehandler = ServiceHandlerFactory(conf, mapfactory, onlineresource, reqparams.get('version', None))
    if reqparams.has_key('version'):
        del reqparams['version']
    if req not in servicehandler.SERVICE_PARAMS.keys():
        raise OGCException('Operation "%s" not supported.' % request, 'OperationNotSupported')
    ogcparams = servicehandler.processParameters(req, reqparams)
    try:
        requesthandler = getattr(servicehandler, req)
    except:
        raise OGCException('Operation "%s" not supported.' % req, 'OperationNotSupported')

    # stick the user agent in the request params
    # so that we can add ugly hacks for specific buggy clients
    ogcparams['HTTP_USER_AGENT'] = request.META['HTTP_USER_AGENT']

    wms_resp = requesthandler(ogcparams)    

    response = HttpResponse()
    response['Content-length'] = str(len(wms_resp.content))
    response['Content-Type'] = wms_resp.content_type
    response.write(wms_resp.content)
        
    return response

def lowerparams(params):
    reqparams = {}
    for key, value in params.items():
        reqparams[key.lower()] = value
    return reqparams