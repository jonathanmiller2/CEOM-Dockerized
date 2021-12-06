from celery import shared_task
import time
import random
import os, sys
import re, glob
import math
import datetime

from ceom.celeryq.modis import products, process, band_names, headers
from ceom.celeryq.modis.aux_functions import latlon2sin
from ceom.celeryq.modis.process import get_pixel_value,get_band_names,gap_fill
from ceom.celeryq.modis.headers import get_modis_header
from collections import OrderedDict
from ceom.celery import app

from django.conf import settings
try:
    from . import database
except Exception as e:
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

def monitor_single_site_tasks(tasks,metadata):
    MAX_ERRORS = 3
    MAX_SECONDS= 200 # seconds
    TIME_CHECK = 1 # seconds
    NUM_STEPS = int(MAX_SECONDS/TIME_CHECK)

    for i in range(0,NUM_STEPS):
        num_tasks = 0
        finished = started = retry = error = pending = 0
        for year,chunks in tasks.items():
            for chunk, task in chunks.items():
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
        print ("Progress: %d Finished: %d Errors: %d Retry: %d Started %d Pending %d " % (progress,finished, error, retry, started, pending)) #This fixed the tuple issue
        if finished + error == num_tasks:
            break
        time.sleep(TIME_CHECK)

def get_data(tasks):
    data = {}
    for year,chunks in tasks.items():
        data[year]={}
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
    return data

# def process_data(data,dataset):
#     return gap_fill(data,dataset)

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
    current_day = datetime.datetime.now().timetuple().tm_yday
    for year in years:
        days = [i+1 for i in range(0,366) if i % dataset_freq_in_days==0]
        if year not in list(range(2000,current_year+1)):
            continue
        if year == 2000:
            days = [day for day in days if day > 56 ] # Modis has no days before this date
        elif year == current_year:
            days = [day for day in days if day <= current_day ] # Cannot get future dates
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
                    'days': [day], 
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

def save_data_multi(data,site_id,dataset,csv_folder,filename,years,write_header=False):
    years = ",".join([str(year) for year in years])
    full_dir = os.path.join(csv_folder)
    full_path = os.path.join(csv_folder,filename)
    if not os.path.exists(full_dir):
        os.makedirs(full_dir)
    f = open(full_path,'a+')
    header = get_header(data,dataset)
    if write_header:
        f.write('site ID,'+','.join([h[1] for h in header])+'\n')
    for year in data:
        for day in sorted([int(day) for day in data[year]]):
            if data[year][str(day)] and len(data[year][str(day)]) == len(header):
                line=[site_id]
                for x in range(0,len(header)):
                    if data[year][str(day)][header[x][0]]:
                        line+=[str(data[year][str(day)][header[x][0]])]
                f.write(','.join(line)+'\n')          
            else:
                current_date = datetime.date(int(year),1,1) + datetime.timedelta(int(day) - 1)
                current_date = current_date.strftime("%m/%d/%Y")
                current_line = [str(site_id),current_date] + ['NA' for x in range(1,len(header))]
                f.write(','.join(current_line)+'\n')
    f.close()
    return filename

def get_file_name(dataset,years):
    years = [str(y) for y in years]
    timestr = dataset+','.join(years)+'_'+time.strftime("%Y-%m-%d_%H:%M:%S")+'.csv'
    return timestr

def read_input_file(file_path):
    print("DIR", os.listdir(os.path.dirname(file_path)))
    print("DIR2", os.path.dirname(file_path))
    f = open(file_path,'r')
    line_cont = 0
    input_sites = OrderedDict()
    # Blank lines counter and boudn to prevent somebody addign 'infinite' blank lines file exploit
    MAX_BLANK_LINES=100
    MAX_SITE_ID_LENGTH = 16
    blank_lines_cont = 0
    # Start reading the file checking for errors first
    for line in f:
        line_cont+=1
        line_data = line.replace('\n','').replace(' ','').split(',')
        if len(line_data)==0 and blanl_lines_cont<MAX_BLANK_LINES:
            # blank line, continue parsing
            blank_lines_cont+=1
            continue
        if len(line_data[0])>MAX_SITE_ID_LENGTH:
            raise Exception('Line %d has a site_id longer than the maximum allowed (%d)'% (line_cont,MAX_SITE_ID_LENGTH))
        if line_data[0] in input_sites:
             raise Exception('Line %d has a duplicated key the site ' % line_cont)
        if len(line_data)!=3:
            raise Exception('Line %d does not contain 3 columns. Correct Format is Unique ID value, Latitude, Longitude eg: 1, 20.2343, -100.26432 ' % line_cont)
        try:
            lat = float(line_data[1])
            lon = float(line_data[2])
        except:
            raise Exception('Line %d latitude or longitude could not be parsed.' % line_cont)
        input_sites[line_data[0]] = {'lat':lat,'lon':lon}
    return input_sites
         
def updateDB(task_id,result,message,progress,total_sites,error=False,working=True):
    try:
        db = database.pgDatabase()
        completed = total_sites==progress
        db.updateMultipleSiteTimeSeries(task_id,result,message,progress,total_sites,completed,error,working)
    except Exception as e:
        print(('Error : %s' % e))
        pass   
@shared_task(time_limit=7200)
def multiple_site_modis(input_file,csv_folder,media_base_url,dataset,years,dataset_npix,dataset_freq_in_days):
    # Get the list days we need to retreive its value, each one of
    # them will be send as an independent task to get their value

    task_id = multiple_site_modis.request.id
    file_result = ''
    message = ''
    try:
        try:
            input_sites = read_input_file(input_file)
        except Exception as e :
            # Set error to the task in the db (Wrong input file)
            #print(("Exception reading input file: ", str(e.message)))
            updateDB(task_id,file_result,str(e.message),0,total_sites,True,False)
            return None;
        time_ini = time.time() # Initial time to extract execution time
        total_sites = len(input_sites)
        multiple_site_modis.update_state(state='STARTED', meta={'completed': 0,'error':0,'total':0,'started':False})
        updateDB(task_id,file_result,message,0,total_sites,False,True)
        filename = get_file_name(dataset,years)
        site_cont=0
        for site_id,site_data in list(input_sites.items()):
            multiple_site_modis.update_state(state='STARTED', meta={'completed': site_cont,'error':0,'total':total_sites,'started':True})
            updateDB(task_id,file_result,message,site_cont,total_sites,False,True)
            site_cont+=1
            lat = site_data['lat']
            lon = site_data['lon']
            metadata = get_location_metadata(lat,lon,dataset,dataset_npix,years) # metadata of the selected site
            # Set task initial state to started
            num_tasks = len(years) # Number of tasks to perform
            multi_day = (int(dataset_freq_in_days)!=1)
            # Send all tasks to queue and store their queing id in a double dictionary (year-->day-->task_id) object
            params_lists = {}
            # Create parameter list for all years
            chunks = 12
            tasks_params = split_tasks_in_chunks(years,metadata,dataset_freq_in_days,multi_day,chunks)
            tasks = send_tasks(get_modis_year_data.delay,tasks_params)
            monitor_single_site_tasks(tasks,metadata)
            data  = get_data(tasks)
            data = gap_fill(data,dataset)
            file_url = save_data_multi(data,site_id,dataset,csv_folder,filename,years,site_cont==1)
            file_result = os.path.join(media_base_url,file_url)
        updateDB(task_id,file_result,message,site_cont,total_sites,False,False)
        time_exec = time.time()-time_ini
        return {'filename':file_url,'exec_time':time_exec}
    except Exception as e:
        updateDB(task_id,file_result,str(e),0,0,True,False)

# ------------------------------------- PROCESSING SCRIPT PART ----------------------------

import multiprocessing as mp
def make_serializable_dict(mydict):
    serialized_dict = OrderedDict()
    for key,value in list(mydict.items()):
        serialized_dict[key] = str(value)
    return serialized_dict

def extract_day_data(col,row,dataset,year,day,tile):
    try:
        multi_day = False
        r = re.compile(".*A(?P<year>\d{4})(?P<day>\d{3}).*.hdf$")
        items = (dataset, year, tile, year, day)
        search = os.path.join(settings.MODIS_DATASETS_PATH, "%s/%d/%s/*%d%03d*.hdf" % items)
        flist = glob.glob(search)
        data = {}

        if len(flist) > 0 and r.match(flist[0]) is not None:
            fn = flist[0]
            pixel_values = None
            try:
                pixel_values = get_pixel_value(fn,col,row)
            except Exception as e:
                print(("Error retrieving pixel values for file: %s %s " % (fn,e.message)))

            data = process.get_dates(pixel_values,year,day,multi_day)
            if products.dataset_is_available(dataset):
               vegetation_indexes = products.get_vegetation_indexes(dataset,pixel_values)
               data = dict(list(data.items())+list(vegetation_indexes.items()))
            data = make_serializable_dict(data)
            data = [(k,v) for k,v in list(data.items()) ]
        else:
            data = None
        return data
    except Exception as e:
        print(("Exception at year %d day %d: %s" % (year,day,e.message)))
        return None


def terminate_task(task_id):
    app.control.revoke(task_id, terminate=True)

@shared_task(time_limit=50)
def get_modis_year_data( params_dict):
    p = params_dict
    results = {p['year']:{}}
    for day in p['days']:
        results[p['year']][day] = extract_day_data(p['col'],p['row'],p['dataset'],p['year'],day,p['tile'])
    return results
