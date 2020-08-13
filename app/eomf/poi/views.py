# Create your views here.
from models import *
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, loader
from forms import AddPixelToResearchForm, ResearchForm,ResearchFormEdit
from django.http import HttpResponse, HttpResponseRedirect
import simplejson
from django.db import connection
from json import dumps, loads, JSONEncoder
from django.core.serializers import serialize
from math import floor, cos, radians,pi
from django.db import connection
from django.core import serializers
from django.contrib.auth.decorators import login_required

def home(request):
    return render_to_response("poi/index.html", {}, context_instance=RequestContext(request))

def wpixel(request):

    t = loader.get_template('poi/what_is_in_pixel.html')
    categories = Category.objects.order_by('order')
    c = RequestContext(request,{
        'categories': categories,
        })
    return HttpResponse(t.render(c))
def latlon2sin(lat,lon,npix):
    cons =(36.0 * npix)/(2.0 * pi)
    yg = 9.0 * npix - radians(cons*lat)
    xg = radians(cons*lon*cos(radians(lat))) + 18.0 * npix
    ih = floor(xg/npix)
    iv = floor(yg/npix)
    x = xg-ih*npix
    y = yg-iv*npix
    xi = floor(x)
    yi = floor(y)
    return {'h': ih, 'v': iv, 'x': xi, 'y': yi}

def getPixelFromLatLon( lat, lon, res_id):
    pixel_dataset = PixelDataset.objects.get(id=res_id)
    npix = pixel_dataset.ncol
    pixel = latlon2sin(lat,lon,npix)
    return Pixel(h=pixel['h'],v=pixel['v'],col=pixel['x'],row=pixel['y'],dataset=pixel_dataset)
def add_research_pixels(request):
   if (request.user.is_authenticated):
        try:
            data=simplejson.loads(request.raw_post_data)
            selected_project_id = int(data['projectId'])
            resolution_id = data['resolution']
            research = Research.objects.get(id=selected_project_id,user=request.user)
            pixels = data['pixels']
            #If user does not own the project or it does not exists it won't get here
            for line in range(0,len(pixels)):
                if len(pixels[line])!=3:
                    errormsg = {
                        'error': "1:User must be logged in and project must belong to him. Data must be included in an array " + str(pixels[line])
                    }
                    return HttpResponse(simplejson.dumps(errormsg))
            #All data is fine, now we need to save it (except for duplicates)
            duplicated = 0;
            pixel_dataset = PixelDataset.objects.get(id=resolution_id)
            npix = pixel_dataset.ncol
            for pixel in pixels:
                # pixel = getPixelFromLatLon(pixel['id'],pixel['lat'],pixel['lon'],resolution_id)
                # 
                id_pix = pixel['id'][0:min(30,len(pixel['id']))]
                lat = float(pixel['lat'])
                lon = float(pixel['lon'])
                cons =(36.0 * npix)/(2.0 * pi)
                yg = 9.0 * npix - radians(cons*lat)
                xg = radians(cons*lon*cos(radians(lat))) + 18.0 * npix
                ih = floor(xg/npix)
                iv = floor(yg/npix)
                x = xg-ih*npix
                y = yg-iv*npix
                xi = floor(x)
                yi = floor(y)
                pixel = {'h': ih, 'v': iv, 'x': xi, 'y': yi}
                try:
                    p = Pixel.objects.get(h=pixel['h'],v=pixel['v'],col=pixel['x'],row=pixel['y'],dataset=pixel_dataset)
                except:
                    p = Pixel(h=pixel['h'],v=pixel['v'],col=pixel['x'],row=pixel['y'],dataset=pixel_dataset)
                    p.save()
                
                try: 
                    rp = ResearchPixel.objects.get(pixel=p,research=research,user=request.user,private_id=id_pix,lat=lat,lon=lon)
                    duplicated = duplicated + 1
                except:
                    rp = ResearchPixel(pixel=p,research=research,user=request.user,private_id=id_pix,lat=lat,lon=lon)
                    rp.save()
            successmsg = {
                'success':"All pixels were saved successfuly",
                'duplicated': duplicated,
                'saved': len(pixels)-duplicated,
                'id':str(data['projectId']),
            } 
            return HttpResponse(simplejson.dumps(successmsg))
        except Exception as e:
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # a = ""+ str(exc_type) + str(fname) + str(exc_tb.tb_lineno)
            #Either project does not exist or user is not the owner of the project. 
            #could modify this part if permissions were required in the future for different users
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            errormsg = {
                'error': "2:User must be logged in and project must belong to him. Data must be included in an array #" + str(e),
                'exc_type':str(exc_type),
                'fname':str(fname),
                'exc_tb.tb_lineno':str(exc_tb.tb_lineno),
            }
            return HttpResponse(simplejson.dumps(errormsg))

def my_custom_sql(sql, params):
    cursor = connection.cursor()
    cursor.execute(sql, params)
    return dictfetchall(cursor)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def get_research_pois(request,research_id):
    if request.user.is_authenticated():
        pois =  ResearchPixel.objects.filter(user=request.user,research_id=research_id)
        pois_serialized = loads(serialize('json', pois,  relations={'pixel':{'relations':('dataset',)},}))
        return HttpResponse(simplejson.dumps(pois_serialized))
    else:
        errormsg = {
                'error': "Must be logged in to retrieve this information"
            } 
        return HttpResponse(simplejson.dumps(errormsg))
@login_required
def create_research(request):
    if request.method == 'POST':
        form = ResearchForm(request.POST)
        form.set_user(request.user)
        t = loader.get_template('poi/addPOIResearch.html')
        if form.is_valid():
            research = Research(name=form.cleaned_data["name"],user=request.user,description=form.cleaned_data["description"])
            try:
                research.save()
                c = RequestContext(request, {
                'form': ResearchForm(request.POST),
                'success': True,
                'saved_research_id': research.id
                })
                return HttpResponse(t.render(c))
            except:
                c = RequestContext(request, {
                    'form': form,
                })
                return HttpResponse(t.render(c))
        else:
            c = RequestContext(request, {
                'form': form,
            })
            return HttpResponse(t.render(c))

    else:
        researchForm = ResearchForm()
        t = loader.get_template('poi/addPOIResearch.html')
        c = RequestContext(request, {'form': researchForm})
        return HttpResponse(t.render(c))
@login_required
def edit_research(request,research_id):
    try:
        research = Research.objects.get(id=research_id,user=request.user)
    except:
        t = loader.get_template('poi/researchNotFound.html')
        c = RequestContext(request, {})
        return HttpResponse(t.render(c))

    if request.method == 'POST':
        form = ResearchFormEdit(request.POST)
        form.set_user(research.user)
        form.set_id(research_id)
        t = loader.get_template('poi/editResearch.html')
        if form.is_valid():
            if (research.name==form.cleaned_data["name"]):
                Research.objects.get(id=research_id,user=request.user).update(description=form.description)
            else:
                Research.objects.get(id=research_id,user=request.user).update(name=form.name,description=form.description)
        c = RequestContext(request, {
        'form': ResearchForm(request.POST),
        'success': True,
        })
        return HttpResponse(t.render(c))

    else:
        researchForm = ResearchFormEdit(initial={'name':research.name,'description':research.description})
        researchForm.set_user(request.user)
        researchForm.set_id(research_id)
        
        t = loader.get_template('poi/editResearch.html')
        c = RequestContext(request, {'form': researchForm})
        return HttpResponse(t.render(c))

@login_required
def manage(request):
    researchs = Research.objects.filter(user=request.user).order_by('name')
    pixel_datasets = PixelDataset.objects.all()
    pixels = None
    if len(researchs)>0:
        pixels = ResearchPixel.objects.filter(research=researchs[0])
    t = loader.get_template('poi/manage.html')
    c = RequestContext(request, {
        'researchs': researchs,
        'pixel_datasets':pixel_datasets,
        'pixels':pixels,
        },
        )
    return HttpResponse(t.render(c))

def addPixelValidation(request):
    a = 1
    try:
        #Make sure that a user is logged in and that the request is AJAX
        # if not request.is_ajax() or not request.user.is_authenticated():
        #     error = {
        #        'error': 'this API requires ajax and use its interface',
        #     }
        #     return HttpResponse(simplejson.dumps(error))
        #Read parameters    
        
        data=simplejson.loads(request.raw_post_data)
        resolution = data["resolution"];
        h = data["h"];
        v = data["v"];
        c = data["col"];
        r = data["row"];
        photo_id = data["photo_id"];
        notes = data["notes"]
        lc1_id = data["lc1_id"];
        lc1_p = data["lc1_p"];
        lc2_id = data["lc2_id"];
        lc2_p = data["lc2_p"];
        lc3_id = data["lc3_id"];
        lc3_p = data["lc3_p"];
        
       

        #Make sure the requests sends accepted reolutions (MODIS for now)
        if resolution not in (1000,500,250):
            error = {
               'error': 'resolution not supported',
            }
            return HttpResponse(simplejson.dumps(error))
        #MAke sure that h,v,c, and r are in proper range
        if h<0 or h>35 or v<0 or v>17:
            error = {
                'error': 'h or v values are out of range',
            }
            return HttpResponse(simplejson.dumps(error))
        if (c<0 or r<0  or (resolution==250 and (c>4800 or r>4800)) or (resolution==500 and (c>2400 or r>2400)) or (resolution==1000 and (c>1200 or r>1200))):
            error = {
                'error': 'c or r values are out of range',
            }
            return HttpResponse(simplejson.dumps(error))
        #Make sure that at least one landover type was sent
        if (lc1_id==None and lc2_id==None and lc3_id==None):
            error = {
                'error': 'no landcover type selected',
            }
            return HttpResponse(simplejson.dumps(error))
        


        #Retrieve required objects
        dataset = PixelDataset.objects.get(pixel_resolution=resolution)
        try:
            photo = Photo.objects.get(id=photo)
        except:
            photo = None
        if (lc1_p!=0 and lc2_p==0 and lc3_p==0):
            # The total percentage must be 100%
            if (lc1_p!=100):
                error = {
                    'error': 'Percentages of all landcover types must sum 100%',
                }
                return HttpResponse(simplejson.dumps(error))
            
            try:
                a=4
                pix = Pixel.objects.get(h=h,v=v,col=c,row=r, dataset=dataset)
            except :
                a = 5
                pix = Pixel(h=h,v=v,col=c,row=r,dataset=dataset)
                pix.save()
            pixelVal = PixelValidation(pixel = pix,user = request.user,notes = notes, photo_used=photo)
            pixelVal.save()
            cat1 = Category.objects.get(id=lc1_id)
            val1 = PixelValidationLandcover(validation = pixelVal,category = cat1, percentage=lc1_p)
            val1.save()
        elif (lc1_p!=0 and lc2_p!=0 and lc3_p==0):
            #All have different landcover types
            if (lc1_id==lc2_id):
                error = {
                    'error': 'landcover types must be different',
                }
                return HttpResponse(simplejson.dumps(error))
            # The total percentage must be 100%
            if (lc1_p+lc2_p!=100):
                error = {
                    'error': 'Percentages of all landcover types must sum 100%',
                }
                return HttpResponse(simplejson.dumps(error))
            #Check if pixel exists in database
            try:
                pix = Pixel.objects.get(h=h,v=v,col=c,row=r, dataset=dataset)
            except :
                pix = Pixel(h=h,v=v,col=c,row=r,dataset=dataset)
                pix.save()
            
            pixelVal = PixelValidation(pixel = pix,user = request.user,notes = notes, photo_used=photo)
            pixelVal.save()
            cat1 = Category.objects.get(id=lc1_id)
            val1 = PixelValidationLandcover(validation = pixelVal,category = cat1, percentage=lc1_p)
            cat2 = Category.objects.get(id=lc2_id)
            val2 = PixelValidationLandcover(validation = pixelVal,category = cat2, percentage=lc2_p)
            val1.save()
            val2.save()
        elif (lc1_p!=0 and lc2_p!=0 and lc3_p!=0):
            if (lc1_id==lc2_id or lc1_id==lc3_id or lc2_id==lc3_id):
                error = {
                    'error': 'landcover types must be different',
                }
                return HttpResponse(simplejson.dumps(error))
            if (lc1_p+lc2_p+lc3_p!=100):
                error = {
                    'error': 'Percentages of all three landcover types must sum 100%',
                }
                return HttpResponse(simplejson.dumps(error))

            # pix = Pixel.objects.get(h=h,v=v=,col=c,row=r,dataset=dataset)
            try:
                pix = Pixel.objects.get(h=h,v=v,col=c,row=r, dataset=dataset)
            except :
                pix = Pixel(h=h,v=v,col=c,row=r,dataset=dataset)
                pix.save()
            pixelVal = PixelValidation(pixel = pix,user = request.user,notes = notes, photo_used=photo)
            pixelVal.save()
            cat1 = Category.objects.get(id=lc1_id)
            val1 = PixelValidationLandcover(validation = pixelVal,category = cat1, percentage=lc1_p)
            cat2 = Category.objects.get(id=lc2_id)
            val2 = PixelValidationLandcover(validation = pixelVal,category = cat2, percentage=lc2_p)
            cat3 = Category.objects.get(id=lc3_id)
            val3 = PixelValidationLandcover(validation = pixelVal,category = cat3, percentage=lc3_p)
            val1.save()
            val2.save()
            val3.save()

        msg = {
                'success': 'Success adding pixel landcover validation',
            } 
        return HttpResponse(simplejson.dumps(msg))
    except :
        exc_type, exc_obj, exc_tb = sys.exc_info()
        errormsg = {
                'error': "Unknown error: %d %s, %s, %s" % (a,exc_type,exc_obj,exc_tb)
            } 
        return HttpResponse(simplejson.dumps(errormsg))

