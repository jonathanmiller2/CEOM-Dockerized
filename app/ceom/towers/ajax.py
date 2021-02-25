import json
from dajaxice.decorators import dajaxice_register
import datetime
import re

@dajaxice_register(method='GET')
def sayhello(request):
	return json.dumps({'message':'Hello World','extra':list(range(2000,2010))})

@dajaxice_register(method='GET')
def getPhoto(request,site_name):
	# Here i do operations with name
	extractedname = site_name
	part2 = re.compile(r'(\w+) ([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2})')
	x = part2.findall(site_name)[0]
	newname = x[0]+"-"+x[1]+"-"+x[2]+x[3]+"-"+x[4]+x[5]+x[6]+".jpg" 
	return json.dumps({'name1':newname,'site_name':site_name})