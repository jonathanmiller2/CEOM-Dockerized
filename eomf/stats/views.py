from django.template import Context, RequestContext, loader, Template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Count
from django.db import connection, transaction
from django.contrib.gis.geos import GEOSGeometry, Polygon, Point
import json as simplejson 

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.files.base import ContentFile
from django.core.files import File
from django.shortcuts import redirect
from django.contrib.auth.models import User


from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import wordwrap
from django.db import connection


import datetime
from datetime import date
import pickle
import itertools
import shutil
import os
import zlib, bz2, pickle, base64, pylzma, binascii


from pykml.factory import KML_ElementMaker as KML
from pykml import parser
from lxml import etree
from django.shortcuts import render

from eomf.accounts.models import Profile
from eomf.photos.models import Photo
from eomf.photos.forms import SearchForm


from django.utils.encoding import smart_str

'''
SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser",
 "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", 
 "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user"
'''
#'select auth_user.id,auth_user.date_joined from auth_user'
#Photo.objects.raw('select photos.id,photos.uploaddate from photos')
# Create your views here.
months_list_names = ['january','february','march','april','may','june','july','august','september','october','november','december']
months_numbers = range(0,12)

def stats_main(request):
	t = loader.get_template('stats/base.html')
	set_user = User.objects.raw('select auth_user.id,auth_user.date_joined from auth_user')
	count, build_cat = getnumusers(set_user)
	c = RequestContext(request,{'test':set_user,'search_yes':False,'count':count, 'build_cat':build_cat, 'cumm':False, 'useryear':True,})
	return HttpResponse(t.render(c))

def getnumusers(set_user):
	data_list = []
	years_users = {}
	build_cat = []
	out_data_list = []
	year1 = 2007;
	year2 = date.today().year
	for profile in set_user:
		data_list.append(profile.date_joined.year)
	for year in range(year1, year2+1):
		build_cat.append(year)
		count = data_list.count(year)
		out_data_list.append(count)
		years_users[year] = count
	return out_data_list, build_cat

#this would be a function to take in year ranges and return the 
def getnumusersbyyear(year1, year2, set_user):
	data_list = []
	years_users = {}
	build_cat = []
	out_data_list = []
	year1 = int(year1)
	year2 = int(year2)
	for profile in set_user:
		data_list.append(profile.date_joined.year)
	for year in range(year1, year2+1):
		build_cat.append(year)
		count = data_list.count(year)
		out_data_list.append(count)
		years_users[year] = count
	return out_data_list, build_cat

def stats_limit(request,year1,year2):
	t = loader.get_template('stats/base.html')
	set_user = User.objects.raw('select auth_user.id,auth_user.date_joined from auth_user')
	count, build_cat = getnumusersbyyear(year1, year2, set_user)
	c = RequestContext(request,{'test':set_user,'count':count,'search_yes':False, 'build_cat':build_cat, 'cumm':False, 'year_range':True, 'year1':year1,'year2':year2,})
	return HttpResponse(t.render(c))

def stats_cumm(request):
	t = loader.get_template('stats/base.html')
	set_user = User.objects.raw('select auth_user.id,auth_user.date_joined from auth_user')
	count, build_cat = getnumusersbyyearcumm(2007, 2016, set_user)
	c = RequestContext(request,{'test':set_user,'search_yes':False,'count':count, 'build_cat':build_cat, 'cumm':True})
	return HttpResponse(t.render(c))

def getnumusersbyyearcumm(year1, year2, set_user):
	data_list = []
	years_users = {}
	build_cat = []
	out_data_list = []
	for profile in set_user:
		data_list.append(profile.date_joined.year)
	for year in range(year1, year2+1):
		build_cat.append(year)
		count = data_list.count(year)
		
		years_users[year] = count
		if year != year1:
			out_data_list.append(count+out_data_list[year-year1-1])
		elif year == year1:
			out_data_list.append(count)
	return out_data_list, build_cat

def stats_limit_mon(request,year1,year2):
	t = loader.get_template('stats/base.html')
	set_user = User.objects.raw('select auth_user.id,auth_user.date_joined from auth_user')
	count, build_cat, data_mon, new_month = getnumusersbymon(year1, year2, set_user)
	c = RequestContext(request,{'new_month':new_month,'search_yes':False,'months_numbers':months_numbers,'months_list_names':months_list_names,'year1':year1,'year2':year2,'data_mon':data_mon,'test':set_user,'count':count, 'build_cat':build_cat, 'cumm':False, 'year_range':True, 'year1':year1,'year2':year2, 'mont':True})
	return HttpResponse(t.render(c))

def stats_limit_mon1(request,mon1,day1,year1,mon2,day2,year2):
	t = loader.get_template('stats/base.html')
	set_user = User.objects.raw('select auth_user.id,auth_user.date_joined from auth_user')
	count, build_cat, data_mon, new_month = getnumusersbymon(year1, year2, set_user)
	c = RequestContext(request,{'new_month':new_month,'search_yes':False,'months_numbers':months_numbers,'months_list_names':months_list_names,'year1':year1,'year2':year2,'data_mon':data_mon,'test':set_user,'count':count, 'build_cat':build_cat, 'cumm':False, 'year_range':True, 'year1':year1,'year2':year2, 'mont':True})
	return HttpResponse(t.render(c))


# data_mon :  dictionary to contain monthly data year passed as a key 
# build_cat : COntains Year information
# count : contains yearly count! so we need only one and 2

def getnumusersbymon(year1, year2, set_user):
	data_list = []
	years_users = {}
	build_cat = []
	peryear_list = []
	out_data_list = []
	year1 = int(year1)
	year2 = int(year2)
	data_mon = {}
	data_list_mon = []
	monthly_count = 0
	monthly_list = []
	rebuild_month_data = []
	for profile in set_user:
		data_list.append(profile.date_joined.year)
	for year in range(year1, year2+1):
		data_list_mon = []
		monthly_list = []
		build_cat.append(year)
		count = data_list.count(year)
		monthly_count = (User.objects.filter(date_joined__year = year))
		for profile1 in monthly_count:
			monthly_list.append(profile1.date_joined.month)
		for month in range(1,13):
			monthly_count = monthly_list.count(month)
			data_list_mon.append(monthly_count)		
		years_users[year] = count
		data_mon[year] = data_list_mon
		if year != year1:
			out_data_list.append(count+out_data_list[year-year1-1])
		elif year == year1:
			out_data_list.append(count)
	for month_data in range(0,12):
		new_list = []
		for year in range(year1, year2+1):
			new_list.append(data_mon[year][month_data])
		rebuild_month_data.append(new_list)
	return out_data_list, build_cat, data_mon, rebuild_month_data
#Cumm : What you See: [9, 26, 56, 113, 243, 437, 611, 682, 555] 
#Norma : What you See: [9, 17, 39, 74, 169, 268, 343, 339, 216
#User.objects.get(date_joined__contains = "2015")
# we need to process info here only --- > Create a new list?  It should contain the data in the format needed. Like month wise.
# month data for the years okay.


def stats_limit_phot1(request,mon1,day1,year1,mon2,day2,year2):
	t = loader.get_template('stats/base.html')
	set_user = Photo.objects.raw('select photos.id,photos.uploaddate from photos')
	count, build_cat, data_mon, new_month = getnumphotosbymon(year1, year2, set_user)
	c = RequestContext(request,{'new_month':new_month,'search_yes':False,'months_numbers':months_numbers,'months_list_names':months_list_names,'year1':year1,'year2':year2,'data_mon':data_mon,'test':set_user,'count':count, 'build_cat':build_cat, 'cumm':False, 'year_range':True, 'year1':year1,'year2':year2, 'phot':True})
	return HttpResponse(t.render(c))

def stats_limit_phot(request,year1,year2):
	t = loader.get_template('stats/base.html')
	set_user = Photo.objects.raw('select photos.id,photos.uploaddate from photos')
	count, build_cat, data_mon, new_month = getnumphotosbymon(year1, year2, set_user)
	c = RequestContext(request,{'new_month':new_month,'search_yes':False,'months_numbers':months_numbers,'months_list_names':months_list_names,'year1':year1,'year2':year2,'data_mon':data_mon,'test':set_user,'count':count, 'build_cat':build_cat, 'cumm':False, 'year_range':True, 'year1':year1,'year2':year2, 'phot':True})
	return HttpResponse(t.render(c))
'''
def getnumphotosbymon(year1, year2, set_user):
	data_list = []
	years_users = {}
	build_cat = []
	out_data_list = []
	year1 = int(year1)
	year2 = int(year2)
	data_mon = {}
	data_list_mon = []
	monthly_count = 0
	monthly_list = []
	rebuild_month_data = []
	for profile2 in Photo.objects.raw('SELECT uploaddate.year FROM Photo')
		data_list.append(profile2.uploaddate.year)				
	for year in range(year1, year2+1):
		data_list_mon = []
		monthly_list = []
		build_cat.append(year)
		count = data_list.count(year)
		monthly_count = (Photo.objects.filter(uploaddate__year = year))
		for profile1 in monthly_count:
			monthly_list.append(profile1.uploaddate.month)
		for month in range(1,13):
			monthly_count = monthly_list.count(month)
			data_list_mon.append(monthly_count)		
		years_users[year] = count
		data_mon[year] = data_list_mon
		if year != year1:
			out_data_list.append(count+out_data_list[year-year1-1])
		elif year == year1:
			out_data_list.append(count)
	for month_data in range(0,12):
		new_list = []
		for year in range(year1, year2+1):
			new_list.append(data_mon[year][month_data])
		rebuild_month_data.append(new_list)
	return out_data_list, build_cat, data_mon, rebuild_month_data
'''
#SELECT "photos"."id", "photos"."location", "photos"."userid", "photos"."photogroupid", 
#"photos"."description", "photos"."long", "photos"."lat", "photos"."regionid", "photos"."takendate", 
#"photos"."time", "photos"."uploaddate", "photos"."datum", "photos"."alt", "photos"."categoryid", 
#"photos"."point", "photos"."dir", "photos"."dir_deg", "photos"."status", "photos"."hash", "
#photos"."source" FROM "photos" WHERE "photos"."uploaddate" BETWEEN 2015-01-01 AND 2015-12-31
#Photo.objects.raw('select Photos.uploaddate, Photos.id from Photos where photos.uploaddate BETWEEN %s AND %s', [year,year])
'''
def getnumphotosbymon(year1, year2, set_user):
	data_list = []
	years_users = {}
	build_cat = []
	out_data_list = []
	year1 = int(year1)
	year2 = int(year2)
	data_mon = {}
	data_list_mon = []
	monthly_count = 0
	monthly_list = []
	rebuild_month_data = []
	for profile2 in set_user:
		data_list.append(profile2.uploaddate.year)				
	for year in range(year1, year2+1):
		data_list_mon = []
		monthly_list = []
		build_cat.append(year)
		count = data_list.count(year)
		monthly_count = (Photo.objects.filter(uploaddate__year = year))
		for profile1 in monthly_count:
			monthly_list.append(profile1.uploaddate.month)
		for month in range(1,13):
			monthly_count = monthly_list.count(month)
			data_list_mon.append(monthly_count)		
		years_users[year] = count
		data_mon[year] = data_list_mon
		if year != year1:
			out_data_list.append(count+out_data_list[year-year1-1])
		elif year == year1:
			out_data_list.append(count)
	for month_data in range(0,12):
		new_list = []
		for year in range(year1, year2+1):
			new_list.append(data_mon[year][month_data])
		rebuild_month_data.append(new_list)
	return out_data_list, build_cat, data_mon, rebuild_month_data
'''
#out_data_list : is cummulative data 
#build_cat : year data the no. of years
#data_mon : is a dictionary that has month data for every year.
#rebuild_month_Data : is something that has 12 lists in it [[]] with all months for all years.
def getnumphotosbymon(year1, year2, set_user):
	build_cat = []
	out_data_list = []
	year1 = int(year1)
	year2 = int(year2)
	data_mon = {}
	rebuild_month_data = []
	build_cat = range(year1,year2+1)
	cursor = connection.cursor()
	cursor.execute('SELECT EXTRACT(YEAR FROM UPLOADDATE) AS YYYY, COUNT(*) AS "PHOTOST" FROM PHOTOS GROUP BY 1 ORDER BY YYYY ASC')
	query1 = cursor.fetchall()
	count = 0
	for year in query1:
		count += int(year[1])
		out_data_list.append(count)
	# clean the out_data_list according to the year1, year2 always
	new_out_data = []
	for year in build_cat:
		new_out_data.append(out_data_list[year-year1])
	out_data_list = new_out_data
	cursor.execute("(SELECT TO_CHAR(UPLOADDATE,'MM-YYYY') AS YEAR_MONTH,COUNT(*) AS PHOTOT FROM PHOTOS GROUP BY 1 ORDER BY YEAR_MONTH ASC) UNION ((SELECT TO_CHAR(DATE,'MM-YYYY') AS YEAR_MONTH,0 AS PHOTOT FROM GENERATE_sERIES('%s-01-01'::TIMESTAMP,'%s-12-31', '1 MONTH' :: INTERVAL) DATE ORDER BY YEAR_MONTH ASC) EXCEPT (SELECT TO_CHAR(UPLOADDATE,'MM-YYYY') AS YEAR_MONTH, 0 AS PHOTOT FROM PHOTOS GROUP BY 1 ORDER BY YEAR_MONTH ASC)) ORDER BY YEAR_MONTH ASC",[year1,year2])
	query2 = cursor.fetchall()
	p = 0
	new_list = []
	for x in query2:
		p = p+1
		if(p == (year2-year1+1)):
			p = 0
			new_list.append(int(x[1]))
			rebuild_month_data.append(new_list)
			new_list = []
		else:
			new_list.append(int(x[1]))
	return out_data_list, build_cat, data_mon, rebuild_month_data


'''SELECT "photos"."id", "photos"."location", "photos"."userid", 
"photos"."photogroupid", "photos"."description", "photos"."long", "photos"."lat", 
"photos"."regionid", "photos"."takendate", "photos"."time","photos"."uploaddate", "photos"."datum", 
"photos"."alt", "photos"."categoryid", "photos"."point", "photos"."dir", "photos"."dir_deg", 
"photos"."status", "photos"."hash", "photos"."source" 
FROM "photos" WHERE "photos"."uploaddate" BETWEEN 2015-01-01 AND 2015-12-31'''

def stats_photo_cumm(request):
	t = loader.get_template('stats/base.html')
	set_user = Photo.objects.raw('select photos.id,photos.uploaddate from photos')
	count, build_cat = getnumphotosbyyearcumm(2007, 2016, set_user)
	c = RequestContext(request,{'test':set_user,'search_yes':False,'count':count, 'build_cat':build_cat, 'cumm':True, 'phot':True})
	return HttpResponse(t.render(c))

def getnumphotosbyyearcumm(year1, year2, set_user):
	build_cat = []
	out_data_list = []
	year1 = int(year1)
	year2 = int(year2)
	data_mon = {}
	rebuild_month_data = []
	build_cat = range(year1,year2+1)
	cursor = connection.cursor()
	cursor.execute('SELECT EXTRACT(YEAR FROM UPLOADDATE) AS YYYY, COUNT(*) AS "PHOTOST" FROM PHOTOS GROUP BY 1 ORDER BY YYYY ASC')
	query1 = cursor.fetchall()
	count = 0
	for year in query1:
		count += int(year[1])
		out_data_list.append(count)
	# clean the out_data_list according to the year1, year2 always
	new_out_data = []
	for year in build_cat:
		new_out_data.append(out_data_list[year-year1])
	out_data_list = new_out_data
	return out_data_list, build_cat

def form_test(request):
	t = loader.get_template('stats/base.html')
	c = RequestContext(request,{'test_form': True,'search_yes':False})
	return HttpResponse(t.render(c))

def search_frm(request):
	photos, search = search_for_photos(request)
	out_data_list, build_cat, data_mon, rebuild_month_data, peryear_list = getSearchData1(photos,2007,2016)
	#out_data_list, build_cat, data_mon, rebuild_month_data, peryear_list = 1,2,3,4,5
	t = loader.get_template('stats/base.html')
	#set_user = User.objects.raw('select auth_user.id,auth_user.date_joined from auth_user')
	#count, build_cat = getnumusers(set_user)
	#c = RequestContext(request,{'test':set_user,'count':count, 'build_cat':build_cat, 'cumm':False})
	c = RequestContext(request,{'peryear':peryear_list,'photos':photos,'search_yes':True, 'search': search, 'count':out_data_list, 'months_list_names':months_list_names,'build_cat':build_cat, 'data_mon':data_mon, 'new_month':rebuild_month_data})
	return HttpResponse(t.render(c))

def getSearchData1(set_user,year1,year2):
	data_list = []
	years_users = {}
	build_cat = []
	out_data_list = []
	year1 = int(year1)
	year2 = int(year2)
	data_mon = {}
	peryear_list = []
	data_list_mon = []
	monthly_count = []
	mon_count = 0
	monthly_list = []
	rebuild_month_data = []
	#cursor = connection.cursor()
	#cursor.execute(str(set_user.query))
	#query1 = cursor.fetchall()
	query1 = set_user
	#set_user = set_user.values('uploaddate')
	for profile2 in query1:
		data_list.append(profile2['uploaddate'].year)				
	for year in range(year1, year2+1):
		data_list_mon = []
		monthly_list = []
		build_cat.append(year)
		count = data_list.count(year)
		monthly_count = []
		for profile2 in query1:
			if profile2['uploaddate'].year == year:
				monthly_count.append(profile2['uploaddate'])
		for profile1 in monthly_count:
			monthly_list.append(profile1.month)
		for month in range(1,13):
			mon_count = monthly_list.count(month)
			data_list_mon.append(mon_count)		
		years_users[year] = count
		data_mon[year] = data_list_mon
		peryear_list.append(count)
		if year != year1:
			out_data_list.append(count+out_data_list[year-year1-1])
		elif year == year1:
			out_data_list.append(count)
	for month_data in range(0,12):
		new_list = []
		for year in range(year1, year2+1):
			new_list.append(data_mon[year][month_data])
		rebuild_month_data.append(new_list)
	return out_data_list, build_cat, data_mon, rebuild_month_data, peryear_list


# form photos views :

def search_for_photos(request):
    photos = Photo.objects.values("uploaddate").order_by('uploaddate').select_related("category__name").reverse()

    if request.user.is_authenticated():
        photos = photos.filter(Q(status=1) | (Q(status=2) & Q(user=request.user)))
    else:
        photos = photos.filter(status=1)

    if request.method == 'POST' or 'query' in request.session:
        if request.method == 'POST':
            search = SearchForm(request.POST)
        else:
            search = SearchForm(pickle.loads(request.session['query']))

        if search.is_valid():
            if request.method == 'POST':
                request.session['query'] = pickle.dumps(request.POST)


            l, t, r, b = -180, 90, 180, -90
            bbox = False
            if search.cleaned_data['lon_min'] is not None:
                l = search.cleaned_data['lon_min']
                bbox = True
            if search.cleaned_data['lon_max'] is not None:
                r = search.cleaned_data['lon_max']
                bbox = True
            if search.cleaned_data['lat_min'] is not None:
                b = search.cleaned_data['lat_min']
                bbox = True
            if search.cleaned_data['lat_max'] is not None:
                t = search.cleaned_data['lat_max']
                bbox = True
            if bbox:
                bbox = Polygon.from_bbox((l, t, r ,b))
                photos = photos.filter(point__bboverlaps=bbox)

            if search.cleaned_data['date_min'] is not None and search.cleaned_data['date_min'] != datetime.datetime(1990,1,1):
                dmin = search.cleaned_data['date_min']
                photos = photos.filter(takendate__gt=dmin)
            if search.cleaned_data['date_max'] is not None and search.cleaned_data['date_max'] != datetime.date.today():
                dmax = search.cleaned_data['date_max']
                photos = photos.filter(takendate__lt=dmax)

            if search.cleaned_data['user'] is not None:
                u = search.cleaned_data['user']
                photos = photos.filter(user__username=u)

            if search.cleaned_data['category'] is not None:
                cat = search.cleaned_data['category']
                photos = photos.filter(category=cat)

            if search.cleaned_data['country'] is not None:
                country = search.cleaned_data['country']
                photos = photos.filter(point__within=country.geometry)

            if search.cleaned_data['continent'] is not None:
                c = search.cleaned_data['continent']
                photos = photos.filter(point__within=c.geometry)

            if search.cleaned_data['keywords'] is not None:
                text = search.cleaned_data['keywords']
                words = text.split()
                for w in words:
                    photos = photos.filter(Q(notes__icontains=w)|Q(file__icontains=w))

    else:
        search = SearchForm()

    return photos, search

