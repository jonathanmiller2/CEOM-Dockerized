import sys, os
sys.path.append('/data1/pavel/dev/')
import process
from django.core.management.base import NoArgsCommand
from eomf.visualization.models import TimeSeriesJob
from eomf.inventory.models import Dataset
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.mail import send_mail

class Command(NoArgsCommand):
    help = 'This command processes time series from top'
    def handle_noargs(self, **options):
            
        try:
            #job = TimeSeriesJob.objects.filter(completed=False).order_by('timestamp')[0:1].get()
            modis = 'myd11a2'
            modis = 'mod09a1'
            points = os.path.join(os.path.dirname(__file__),"test_points.txt")
            years = ['2007','2008']
            ds = Dataset.objects.filter(name=modis)[0]
            #print ds.xdim
            process.npix = int(ds.xdim)
            #process.debug = True
            
            print process.process_job(points,years,modis)
            
        except ObjectDoesNotExist:
            pass
            print 'No jobs to process'

