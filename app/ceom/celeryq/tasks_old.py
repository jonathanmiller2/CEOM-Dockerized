from celery import task
from celery import Celery
import time 
import random
import os, sys
import re, glob
import math, datetime

from .modis import products, process, band_names, headers
from .modis.aux_functions import latlon2sin
from .modis.process import get_pixel_value,get_band_names

app = Celery('tasks', backend='amqp', broker='amqp://')
app.config_from_object('celeryconfig')

MAX_ERRORS = 0
MAX_SECONDS= 100 # seconds
TIME_CHECK = 0.5 # seconds
NUM_STEPS = int(MAX_SECONDS/TIME_CHECK)
@app.task(bind=True)
def get_modis_raw_data(self,csv_folder,lat,lon,dataset,years,dataset_npix,dataset_freq_in_days,vi = True):
    # Get the list days we need to retreive its value, each one of
    # them will be send as an independent task to get their value

    time_ini = time.time()
    ih, iv, xi, yi, folder = latlon2sin(float(lat), float(lon), dataset, dataset_npix)
    metadata = {
        'lat': lat,
        'lon': lon,
        'tile': 'h%02dv%02d' % (ih,iv),
        'dataset':dataset,
        'col':xi,
        'row':yi
    }
    get_modis_raw_data.update_state(state='STARTED', meta={'completed': 0,'error':0,'total':0,'started':False,'metadata':metadata})
    days = [i+1 for i in range(0,366) if i%dataset_freq_in_days==0]
    num_tasks = 0 # Number of tasks to perform
    # multi_day is used to know erther the field real_date will be in modis bands
    multi_day = (int(dataset_freq_in_days)!=1)
    tasks={}
    num_errors = {} # Number of times the task failes <= MAX_ERRORS
    fatal_failures = {} # Tasks that failed MAX_ERRORS times and won't be rerunned
    fatal_failures_counter=0
    # Send all tasks to queue and store their queing id in a double dictionary (year-->day-->task_id) object
    for year in years:
        tasks[year]={}
        num_errors[year]={}
        fatal_failures[year]={}
        for day in days:
            if year==2000 and day < 49:
                continue
            num_tasks += 1
            tasks[year][day] = get_modis_day_data.delay(ih, iv, xi, yi, folder,dataset,year,day,vi,multi_day)
            num_errors[year][day] = fatal_failures[year][day] = 0
    get_modis_raw_data.update_state(state='STARTED', meta={'completed': 0,'error':0,'total':num_tasks,'started':True,'metadata':metadata})
    for i in range(0,NUM_STEPS):
        finished = started = retry = error = pending = 0
        for year,days_dict in list(tasks.items()):
            for day,task in list(days_dict.items()):
                state = task.state
                finished += state=='SUCCESS' # When task finished
                started += state=='STARTED'   #When task is started
                retry += state=='RETRY' # When task failed to send
                error +=  state=='FAILURE' #Task had an error
                pending += state=='PENDING' # Task is pending to be processed from the queue
                if tasks[year][day].state=='FAILURE':
                    if num_errors[year][day] < MAX_ERRORS:
                        tasks[year][day] =  get_modis_day_data.delay(ih, iv, xi, yi,folder,dataset,year,day,vi,multi_day)
                        num_errors[year][day] += 1
                    elif not fatal_failures[year][day]:
                        fatal_failures[year][day] = 1
                        fatal_failures_counter+=1
        total_finished = finished + fatal_failures_counter
        progress = int((float(total_finished)/num_tasks)*100)
        print(("Progress: %d Finished: %d Errors: %d Retry: %d Started %d Pending %d ") % (progress,finished, error, retry, started, pending))

        get_modis_raw_data.update_state(state='STARTED',  meta={'completed': finished,'error':fatal_failures_counter,'total':num_tasks,'metadata':metadata})

        if total_finished==num_tasks:
            break
        time.sleep(TIME_CHECK)
    result = {}
    data = {}
    for year,days_dict in list(tasks.items()):
        data[year] = {}
        for day,task in list(days_dict.items()):
            if task.state== 'SUCCESS':
                data[year][day] = task.result
                task.forget()
            else:
                data[year][day] = None
                task.forget()
    # Gap fill data
    data = process.gap_fill(dataset,data)
    # Now get variable ready to create the csv file
    file_name= str(self.request.id)+'.csv'
    filepath = os.path.join(csv_folder,file_name)

    # Need to get the order of the header
    sample = get_sample(data)
    header = get_header(dataset,sample,vi)
    save_data_to_csv(data,header,filepath)
    # Processing finished 
    time_exec = time.time() - time_ini
    # Store metadata in the result
    result['filename']=file_name
    result['metadata']=metadata
    result['report']={
        'completed': finished,
        'errors': fatal_failures_counter,
        'total':num_tasks,
        'time_exec': time_exec
    }
    return result
def get_sample(data):
    for year in sorted(data.keys()):
        for day in sorted(data[year].keys()):
            if data[year][day] is not None:
                return data[year][day]
    raise Exception('There is no data available')

def get_header(dataset,sample,vi=True):
    if dataset.upper()=='MOD09A1':
        return headers.get_modis_header(dataset,vi)
    else:
        return get_band_names_list_from_dict(sample)

def get_band_names_list_from_dict(dict_sample):
    excluded_keys = ('date','real_date')
    result = [('date','Date'),('real_date','Actual_date')]
    for key in sorted(dict_sample.keys()):
        if key not in excluded_keys:
            result.append((key,key))
    return result

def save_data_to_csv(data, header, filepath):
    try:
        f = open( filepath, 'w' )
        # Write header
        header_titles = [ header_tuple[1] for header_tuple in header]
        header_names = [ header_tuple[0] for header_tuple in header]
        f.write(','.join(header_titles)+"\n")
        # Write body
        for year in sorted(data.keys()):
            for day in sorted(data[year].keys()):
                line=[]
                for column in range(0,len(header_names)):
                    try:
                        line.append(str(data[year][day][header[column][0]]))
                    except:
                        line.append('NA')
                f.write(','.join(line)+"\n")
        f.close()
    except Exception as e:
        raise Exception( "Error saving the csv file: [%s] " % (e.message))
        
    return True


# ------------------------------------- PROCESSING SCRIPT PART ----------------------------
MODIS_FOLDER_PATH = "/data/vol01/modis/"

@app.task()
def get_modis_day_data( ih, iv, xi, yi, folder,dataset, year, day,  vi = False, multi_day=True):

    r = re.compile(".*A(?P<year>\d{4})(?P<day>\d{3}).*.hdf$")
    
    items = (dataset, year, folder, year, day)
    search = MODIS_FOLDER_PATH+"%s/%d/%s/*%d%03d*.hdf" % items
    flist = glob.glob(search)
    data = {}
    if len(flist) > 0:
        fn = flist[0]
        try:
            pixel_values = get_pixel_value(fn,xi,yi)
        except Exception as e:
            raise Exception("Error retrieving pixel values for file: %s %s " % (fn,e.message))
        m = r.match(fn)
        if m is None:
            raise Exception('Error matching regex')

        data = process.get_dates(dataset,pixel_values,year,day,multi_day)
        if vi and products.dataset_is_available(dataset):
           vegetation_indexes = products.get_vegetation_indexes(dataset,pixel_values)   
           data = dict(list(data.items())+list(vegetation_indexes.items()))  
        data = make_serializable_dict(data)
        return data
    else:
        raise Exception('No files found for %s' % (search))

def make_serializable_dict(mydict):
    for key,value in list(mydict.items()):
        mydict[key] = str(value)
    return mydict


# For testing purposes (control)
if __name__ == "__main__":
    lat =  42.587495
    lon = -104.828119
    dataset= 'mod11a1'
    dataset_freq_in_days=1
    years = [2010,]
    vi = False
    dataset_npix = 1200
    csv_folder = '/webapps/ceom_admin/celeryq/tests'
    pixel_val = get_modis_raw_data.delay(csv_folder,lat,lon,dataset,years,dataset_npix,dataset_freq_in_days,vi)

# For testing purposes (worker)
# if __name__ == "__main__":
#     sys.path.append('/home/menarguez/celeryq/ceom-celery')
#     lat =  40.492649
#     lon = -98.321838
#     dataset= 'mod11a1'
#     year = 2010
#     vi = True
#     dataset_npix = 1200
#     day = 9
#     multi_day = False
#     ih, iv, xi, yi, folder = latlon2sin(float(lat), float(lon), dataset, dataset_npix)
#     result = get_modis_day_data(ih, iv, xi, yi, folder,dataset,year,day,vi,multi_day)
#     print result