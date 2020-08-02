import sys, os
sys.path.append('/web/eomf/lib/')
import process
from django.core.management.base import NoArgsCommand
from visualization.models import TimeSeriesJob
from inventory.models import Dataset
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.mail import send_mail

class Command(NoArgsCommand):
    help = 'This command processes time series from top'
    def handle_noargs(self, **options):
        print "executing command"
        try:
            count = TimeSeriesJob.objects.filter(working=True).count()
            if count > 0:
                sys.exit(1)

            job = TimeSeriesJob.objects.filter(completed=False,error=False).order_by('timestamp')[0:1].get()
            if job.working:
                sys.exit(1)
            else:
                print ""
                job.working = True
                job.save()

            modis = str(job.product)
            points = str(job.points.path)
            years = job.years.split(',')
            name = os.path.basename(points)
            mail_recipients=[job.user.email]
            if job.sender and job.sender!="":
                mail_recipients.append(job.sender)
            ds = Dataset.objects.filter(name=modis)[0]
            process.npix = int(ds.xdim)
            
            try:       
                if modis=='mod09a1':     
                    data = process.process_job_with_products(points,years,modis)
                else:
                    data = process.process_job(points,years,modis)
                cont = ContentFile(data)
                job.completed = True
                job.working = False
                job.result.save(name, cont, save=True)
                job.save()
                
                msg =  "Input file processed: http://eomf.ou.edu"+job.points.url+"\n"
                msg += "Results can be downloaded at http://eomf.ou.edu"+job.result.url+"\n"
                msg += "Thank you for using our services\n\n"
                msg += "EOMF team"
                send_mail("Timeseries completed: "+name, msg, "noreply@eomf.ou.edu", mail_recipients, fail_silently=False)
                       #Undefined error occured 
            except Exception, e:
                print str(e)
                job.completed = False
                job.working = False
                job.error = True
                job.save()
 
        except ObjectDoesNotExist:
            print 'No jobs to process'
            pass
