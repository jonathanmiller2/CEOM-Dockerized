from django.template import Context, RequestContext, loader, Template
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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
import itertools
import shutil
import os
import zlib, bz2, pickle, base64, pylzma, binascii


from pykml.factory import KML_ElementMaker as KML
from pykml import parser
from lxml import etree
from django.shortcuts import render

from ceom.accounts.models import Profile
from ceom.photos.models import Photo
from ceom.photos.forms import SearchForm
from ceom.towers.models import phenocam


from django.utils.encoding import smart_str


def tower_main(request):
	x_axis = []
	y_axis = []
	iget_data = phenocam.objects.values('sitename','takendate','gcc').all()
	for x in iget_data:
		x_val = x['sitename'].encode("ascii")+" "+str(x['takendate']).encode("ascii")
		#x_val = str(x_val)
		y_val = float(x['gcc'])
		x_axis.append(x_val)
		y_axis.append(y_val)
	x_axis = str(x_axis)
	return render(request, 'towers/base.html', context={'x_val':x_axis,'y_val':y_axis,})