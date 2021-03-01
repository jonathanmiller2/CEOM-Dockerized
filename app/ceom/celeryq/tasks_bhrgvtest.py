
from celery import task
from celery import Celery
import time
import random
import os, sys
import re, glob
import math
import datetime

from .modis import products, process, band_names, headers
from .modis.aux_functions import latlon2sin
from .modis.process import get_pixel_value,get_band_names,gap_fill
from .modis.headers import get_modis_header
from collections import OrderedDict
app = Celery('tasks', backend='amqp', broker='amqp://')
app.config_from_object('celeryconfig')

from celery import group

try:
    from . import database
except:
    print("Database.py not found. disregard if it is a worker process")

def get_location_metadata(lat,lon,dataset,dataset_npix,years):
    ih, iv, xi, yi, folder = latlon2sin(float(lat), float(lon), dataset, dataset_npix)
    metadata = {
        'lat': lat,
        'lon': lon,
        'tile': 'h%02dv%02d' % (ih,iv),
        'dataset':dataset,
        'col':xi,
        'row':yi,
        'years':years
    }
    return metadata

def monitor_tasks(tasks,fun,metadata):
    MAX_ERRORS = 3
    MAX_SECONDS= 1000 # seconds
    TIME_CHECK = 1 # seconds
    NUM_STEPS = int(MAX_SECONDS/TIME_CHECK)

    for i in range(0,NUM_STEPS):
        num_tasks = 0
        finished = started = retry = error = pending = 0
        for year,chunks in tasks.items():
            for chunk, task in chunks.items():
                print("task_debug:")
                print(task.state)
                num_tasks+=1
                state = task.state
                finished += state=='SUCCESS' # When task finished
                started += state=='STARTED'  # When task is started
                retry += state=='RETRY'      # When task failed to send
                error +=  state=='FAILURE'   # Task had an error
                pending += state=='PENDING'  # Task is pending to be processed from the queue
                # if state==u'FAILURE':
                #     if curret_year_errors < MAX_ERRORS:
                #         tasks[year][day] =  get_modis_year_data.delay(ih, iv, xi, yi,folder,dataset,year,dataset_freq_in_days,vi,multi_day)
                #         num_errors[year][day] += 1
                #     elif not fatal_failures[year][day]:
                #         fatal_failures[year][day] = 1
                #         fatal_failures_counter+=1
        progress = int((float(finished + error)/num_tasks)*100)
        print(("Progress: %d Finished: %d Errors: %d Retry: %d Started %d Pending %d ") % (progress,finished, error, retry, started, pending))
        fun.update_state(state='STARTED',  meta={'completed': finished,'error':error,'total':num_tasks,'metadata':metadata})
        if finished + error == num_tasks:
            break
        time.sleep(TIME_CHECK)

def get_data(tasks):
    data = {}
    for year,chunks in tasks.items():
        data[year]={}
        try:  
            for chunk, task in chunks.items():
                state = task.state
                if state!='SUCCESS':
                    # data[year].update{''}
                    # Should set to none or error the days of this tasks
                    pass
                else:
                    bands_dict={}

                    for day, day_data_list in list(task.result[str(year)].items()):
                        if day_data_list:
                            bands_dict [day] = OrderedDict(day_data_list)
                        else:
                            bands_dict [day] = None
                    data[year].update(bands_dict) #Merge the partial year dict into the global year dict
                    task.forget() #Remove partial info from backend because it is no longer necessary
        except:
            print("debug: 2")
            pass            
    return data

def process_data(data,dataset):
	print("iam in PROCESS DATA ******************")
	print("data:")
	#print data
	print("dataset:")
	print(dataset)
	return gap_fill(data,dataset)

def send_tasks(function, params_dict):
    tasks =  {}
    for year,chunks in params_dict.items():
        tasks[year]={}
        for chunk, param_dict in chunks.items():
            tasks[year][chunk] = function(*[param_dict])
    return tasks

def split_tasks_in_chunks(years,metadata,dataset_freq_in_days,multi_day,num_chunks=5):
    task_params = dict([(year,{}) for year in years])
    current_year = datetime.datetime.now().year
    current_doy = datetime.datetime.now().timetuple().tm_yday
    for year in years:
        days = [i+1 for i in range(0,366) if i % dataset_freq_in_days==0]
        if year not in list(range(2000,current_year+1)):
            continue
        if year == 2000:
            days = [day for day in days if day > 56 ] # Modis has no days before this date
        elif year == current_year:
            days = [day for day in days if day <= current_doy ] # Cannot get future dates
        for day in days:
            chunk = ((day-1)/dataset_freq_in_days) % num_chunks
            if chunk not in task_params[year]:
                task_params[year][chunk] = {
                    'col' :     metadata['col'],
                    'row' :     metadata['row'],
                    'tile':     metadata['tile'],
                    'dataset':  metadata['dataset'],
                    'year':     year,
                    'dataset_freq_in_days': dataset_freq_in_days,
                    'multi_day': multi_day,
                    'days': [day,]
                }
            else:
                task_params[year][chunk]['days']+=[day]
    return task_params

def get_header(data,dataset):
    if dataset.upper()=='MOD09A1':
        return get_modis_header(dataset,True)
    for year in data:
        for day in sorted(data[year]):
            if data[year][str(day)]:
                header=[]
                for band in data[year][str(day)]:
                    if band:
                        header+=[(band,band)]
                return header
    raise Exception ('Error getting header')

def save_data(data,csv_folder,task_id,metadata):
    years = ",".join([str(year) for year in metadata['years']])
    filename = metadata['dataset']+"_lat_"+str(str(metadata['lat']))+"_lon_"+str(str(metadata['lon']))+'_years_'+years+'.csv'
    full_path = os.path.join(csv_folder,filename)
    f = open(full_path,'w')
    header = get_header(data,metadata['dataset'])
    f.write(','.join([h[1] for h in header])+'\n')
    for year in data:
        for day in sorted([int(day) for day in data[year]]):
            if data[year][str(day)] and len(data[year][str(day)]) == len(header):
                line=[]
                for x in range(0,len(header)):
                    if data[year][str(day)][header[x][0]]:
                        line+=[str(data[year][str(day)][header[x][0]])]
                f.write(','.join(line)+'\n')          
            else:
                current_date = datetime.date(int(year),1,1) + datetime.timedelta(int(day) - 1)
                current_date = current_date.strftime("%m/%d/%Y")
                current_line = [current_date] + ['NA' for x in range(1,len(header))]
                f.write(','.join(current_line)+'\n')
    f.close()
    return filename


@app.task(bind=True)
def get_modis_raw_data(self,csv_folder,media_base_url,lat,lon,dataset,years,dataset_npix,dataset_freq_in_days):
    # Get the list days we need to retreive its value, each one of
    # them will be send as an independent task to get their value
    time_ini = time.time() # Initial time to extract execution time
    print("get_modis_raw_data:")
    metadata = get_location_metadata(lat,lon,dataset,dataset_npix,years) # metadata of the selected site
    print(metadata)
    # Set task initial state to started
    get_modis_raw_data.update_state(state='STARTED', meta={'completed': 0,'error':0,'total':0,'started':False,'metadata':metadata})
    num_tasks = len(years) # Number of tasks to perform
    multi_day = (int(dataset_freq_in_days)!=1)
    # Send all tasks to queue and store their queing id in a double dictionary (year-->day-->task_id) object
    params_lists = {}
    # Create parameter list for all years
    chunks = 12
    tasks_params = split_tasks_in_chunks(years,metadata,dataset_freq_in_days,multi_day,chunks)
    print("Sending tasks to queue:")
    # tasks = send_tasks(get_modis_year_data.delay,tasks_params)
    tasks = send_tasks(get_modis_year_data,tasks_params)
    print('Monitoring tasks')
    # remove comments later
    try:
        monitor_tasks(tasks,self,metadata)
    except:
        pass
    try:
        data  = get_data(tasks)
    except:
        pass
    print('Processing data')
    data = process_data(data,dataset)
    print('saving data')
    filename = save_data(data,csv_folder,get_modis_raw_data.request.id,metadata)
    try:
        db = database.pgDatabase()
        db.updateCompletedSingleTimeSeriestask(get_modis_raw_data.request.id,os.path.join(media_base_url,filename),)
    except Exception as e:
        print('Error : %s' % e.message)
        pass
    return {'filename':filename,'metadata':metadata,}

# ------------------------------------- PROCESSING SCRIPT PART ----------------------------
MODIS_FOLDER_PATH = "/data/ifs/modis/datasets/"

import multiprocessing as mp
def make_serializable_dict(mydict):
    serialized_dict = OrderedDict()
    for key,value in list(mydict.items()):
        serialized_dict[key] = str(value)
    return serialized_dict

def extract_day_data(col,row,dataset,year,day,tile):
    print("I'm in extract_day_data:")
    try:
        multi_day = False
        print("Getting day: %d" % day)
        r = re.compile(".*A(?P<year>\d{4})(?P<day>\d{3}).*.hdf$")
        items = (dataset, year, tile, year, day)
        search = MODIS_FOLDER_PATH+"%s/%d/%s/*%d%03d*.hdf" % items
        flist = glob.glob(search)
        data = {}
        print("file list debug")
        print(flist)
        if len(flist) > 0 and r.match(flist[0]) is not None:
            fn = flist[0]
            pixel_values = None
            try:
                pixel_values = get_pixel_value(fn,col,row)
            except Exception as e:
                print("Error retrieving pixel values for file: %s %s " % (fn,e.message))

            data = process.get_dates(pixel_values,year,day,multi_day)
            if products.dataset_is_available(dataset):
               vegetation_indexes = products.get_vegetation_indexes(dataset,pixel_values)
               data = dict(list(data.items())+list(vegetation_indexes.items()))
            data = make_serializable_dict(data)
            data = [(k,v) for k,v in list(data.items()) ]
        else:
            data = None
            print("i entered else part because i have no files or files returned were 0")
        return data
    except Exception as e:
        print("Exception at year %d day %d: %s" % (year,day,e.message))
        return None

@app.task(time_limit=50)
def get_modis_year_data( params_dict):
    print("I'm in get_modis_year_data:")
    p = params_dict
    results = {p['year']:{}}
    for day in p['days']:
        results[p['year']][day] = extract_day_data(p['col'],p['row'],p['dataset'],p['year'],day,p['tile'])
    return results

# For testing purposes (control)

if __name__ == "__main__":
    # lat =  43.587495
    # lon = -102.828119
    # dataset= 'mod09a1'
    # dataset_freq_in_days=8
    # years = range(2000,2015)
    # dataset_npix = 1200
    lat =  0.820435
    lon = 109.688242
    dataset= 'mod09a1'
    dataset_freq_in_days=8
    years = list(range(2009,2010))
    dataset_npix = 1200
    csv_folder = '/webapps/ceom_admin/celeryq/tests'
    # pixel_val = get_modis_raw_data.delay(csv_folder,csv_folder,lat,lon,dataset,years,dataset_npix,dataset_freq_in_days)
    pixel_val = get_modis_raw_data(csv_folder,csv_folder,lat,lon,dataset,years,dataset_npix,dataset_freq_in_days)
    print("i entered main and returning just none:")
    print(pixel_val)
    # print pixel_val.result

def terminate_task(task_id):
    app.control.revoke(task_id, terminate=True)

# For testing purposes (worker)
# if __name__ == "__main__":
#     sys.path.append('/home/menarguez/celeryq/ceom-celery')
#     lat =  40.492649
#     lon = -98.321838
#     dataset = 'mod09a1'
#     dataset_npix = 1200
#     col, row, xi, yi, tile = latlon2sin(float(lat), float(lon), dataset, dataset_npix)
#     params = {
#         'col' :  col,
#         'row' : row,
#         'tile' : tile,
#         'dataset' : dataset,
#         'year' : 2007,
#         'dataset_freq_in_days': 8,
#         'multi_day' : 8,
#         'days' : [i for i in range (1,40,8)]
#     }
    
    
#     result = get_modis_year_data(params)
#     print result
