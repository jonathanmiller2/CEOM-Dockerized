# This Python file uses the following encoding: utf-8
import sys, os
from datetime import datetime
from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.contrib.gis.db import models

#from geohealth.models import Birds
#il = list(Birds.objects.all())
#objects = Birds.objects.order_by("animal","gmt_date").distinct("animal","gmt_date")
from django.contrib.auth.models import User
from accounts.models import Profile, user_post_save
from accounts.fields import COUNTRIES
from photos.models import Photo, PhotoUser
objects = PhotoUser.objects.all().filter(id__gt=760)
l = list(objects)
print len(l)

models.signals.post_save.disconnect(user_post_save, User)

for pu in l:
    u = User() 
    u.id = pu.id
    u.username = pu.username
    u.password = pu.password
    u.email = pu.email
    u.date_joined = pu.createdate
    if type(pu.timestamp) == int:
        u.last_login = datetime.fromtimestamp(pu.timestamp)
    
    if pu.name is not None:
        names = pu.name.strip().split(' ',1)
        for n in names:
            if len(n) > 29:
                print n
                
        if len(names) == 1:
            u.first_name = names[0].strip()
    
        elif len(names) == 2:
            u.first_name = names[0].strip()
            u.last_name = names[1].strip()
            
    
    u.save()
    
    p = Profile()
    p.id = pu.id
    p.user = u
    p.affiliation = pu.affiliation
    p.address1 = pu.address1
    p.address2 = pu.address2
    p.postal = pu.postal
    p.state = pu.state
    p.telephone = pu.telephone
    
    if pu.country is not None:
        found = False
        puc = pu.country.lower().strip()
        if "china" in puc:
            puc = 'china'
        elif puc in ('us', 'usa', 'amerika', 'united states', 'united sates','u.s.a.'):
            puc = 'united states of america'
        elif puc in ('uk',):
            puc = "united kingdom"
        elif puc in (u'việt nam', 'vietnam'):
            puc = "viet nam"
            
        for c in COUNTRIES:
            if c[1].lower() == puc:
                p.country = c[0]
                found = True
        if not found:
            p.country = None
            
    p.save()
    #print u.__dict__
    #print p.__dict__
    
    #if i > 10:
    #    sys.exit()
    #else:
    #    i += 1
