from modis.special_products import mod09a1
from collections import  OrderedDict
import datetime
REAL_DATE_BAND_NAME = 'sur_refl_day_of_year'
try:
    from osgeo import gdal
    from osgeo.gdalconst import GA_ReadOnly
except:
    pass
def get_dates(data,year,day,multi_day=True): 
    new_dict = OrderedDict()
    date = datetime.date(int(year),1,1) + datetime.timedelta(int(day) - 1)
    new_dict['date'] = date.strftime("%m/%d/%Y")
    if multi_day:
        new_dict['real_date']  = (datetime.date(int(year),1,1)+datetime.timedelta(int(data[REAL_DATE_BAND_NAME])-1)).strftime("%m/%d/%Y")
    else:
        new_dict['real_date'] = new_dict['date']
    for k,e in data.items():
        if k not in ('date',REAL_DATE_BAND_NAME):
            new_dict[k] = e
    return new_dict

def get_band_names(filename):
    ds = gdal.Open(filename, GA_ReadOnly)
    if ds is None:
        raise Exception('Error opening file')
    # Need to open file to read all band names
    subdata = ds.GetSubDatasets()
    bands = [ band_data[0].replace('"','') for band_data in subdata]
    band_names = [ band_data[0].split(':')[-1:][0] for band_data in subdata]
    ds=None #Close dataset
    return band_names,bands

def get_pixel_value(filename,row,column):
    filename = str(filename)
    band_names,bands = get_band_names(filename)
    pixel_value = OrderedDict()
    for i in range(0,len(bands)):
        ds = gdal.Open(bands[i], GA_ReadOnly)
        pixel_value[band_names[i]] = ds.GetRasterBand(1).ReadAsArray(row,column,1,1)[0][0] # TODO Check if start from 0 or from 1 row and column
        ds = None # Close dataset
    return pixel_value


def set_gf_no_gf(data_dict,relation_dict,gf_key,gf_value):
    result = data_dict
    result[gf_key] = gf_value
    for (key, value) in relation_dict:
        result[value] = result[key]
    return result

def set_gf(data_dict,relation_dict,ini_dict,end_dict,num_bad_obs,pos,gf_key,gf_value):
    print('\033[95m'+"~~~~~~~~~~~~~~~~~~~~~Filling GAP fill values USING set_gf method~~~~~~~~~~~~~~~~~~~~~~~"+'\033[0m')
    #print("Gap FIlling the Following:"
    #"start:"+str(ini_dict)+"end:"+str(end_dict)+
    print('\033[93m'+"start:\t"+"num_bad_obs:"+str(num_bad_obs)+"\tpos:"+str(pos)+"\tgf_key:"+str(gf_key)+"\tgf_value:\t"+str(gf_value)+'\033[0m')
    result = data_dict
    result[gf_key] = gf_value
    pos = float(pos)
    print("**working/producing gap fills**")
    print("******************************************************************************************************************")
    for (key, value) in relation_dict:
        try:
            ini = float(ini_dict[key])
            end = float(end_dict[key])
            result[value] = ini+((end-ini)*pos/float(num_bad_obs+1))
            print('\033[91m'+"\t\tini:  "+str(ini)+"\tend:  "+str(end)+"\tresult:  "+str(result[value])+"\tkey:  "+str(key)+"\tvalue:  "+str(value)+'\033[0m')
        except:
            # Evi can have initial or end value = None due to division by zero
            print("\t\t iam in the EVI exempt part")
            result[value] = result[key]
            result[gf_key] = 'NA'
            print("\t\tresult:  "+str(result[value])+"\tgf_key:  "+str(result[gf_key]))
    print("******************************************************************************************************************")
    return result

MAX_BAD_OBS = 4

def gap_fill_algorithm(data,relation_dict,is_bad_observation,gf_key):
    print(" -------------*************i am in gap fill algorithm: *************------------------")
    bad_observations = []
    print("bad_obs:***")
    print(bad_observations)

    ini_good_obs = None

    for year in sorted(data.keys()):
        print("year:\t"+str(year)+"->")
        print(sorted(data[year].keys()))
        print([unicode(str(day)) for day in sorted([int(day.encode('UTF8')) for day in data[year].keys()])])
        for day in [unicode(str(day)) for day in sorted([int(day.encode('UTF8')) for day in data[year].keys()])]:
            print("\t"+"day:\t"+str(day)+"->")

    for year in sorted(data.keys()):
        print("year:\t"+str(year)+"->")
        for day in [unicode(str(day)) for day in sorted([int(day.encode('UTF8')) for day in data[year].keys()])]:
            print("\t"+"day:\t"+str(day)+"->")
            # this if condioton is applicable if data is not there
            #day = str(day)
            if data[year][day] is None:
                print("\t\tdata in this is none")
                # Data is missing for this day, cannot gap fill previous obs nor next ones until a good obs is found
                ini_good_obs = None
                for (y,d) in bad_observations:
                    print("year:\t"+str(y)+"\tday:\t"+str(d)+"   is set to no gap fill")
                    data[y][d] = set_gf_no_gf(data[y][d],relation_dict,gf_key,"NA")
                bad_observations = []
            # this elif condition makes sense when data is there and is a bad observation
            elif is_bad_observation(data[year][day]):
                print("\t\tthis day is a bad observation")
                bad_observations.append((year,day))
                data[year][day]['bad_obs'] = 'Yes'
            #else there is data and not a bad observation we do the following
            else:
                print("\t\t this observation is good")
                data[year][day]['bad_obs'] = 'No'
                # check if this is the first good observation we have
                print("\t\t1. as length of bad observations is:\t"+str(len(bad_observations))+'\033[0m')
                if ini_good_obs is None:
                    # This is the first good observation, check if we have bad obs before
                    print('\033[1m'+"\t\t\tThere is no initial value"+'\033[0m')
                    if len(bad_observations)>0:
                        print('\033[4m'+"\t\t\t\t i cannot fill previous because there is no initial value for  for these bad obs"+'\033[0m')
                        # We cannot gap fill previous bad obs because there is no initial value
                        for (y,d) in bad_observations:
                            data[y][d] = set_gf_no_gf(data[y][d],relation_dict,gf_key,"NA")
                # now it checks the length of bad observations on ly if the length of bad obs are greater than 0 and less than max and if ithere is an initial value
                elif len(bad_observations)>0 and len(bad_observations) <= MAX_BAD_OBS:
                    print('\033[1m'+"\t\t\t2. as length of bad observations is:\t"+str(len(bad_observations))+'\033[0m')
                    # Gap fill bad obs
                    last_good_obs = data[year][day]
                    pos=0
                    for (y,d) in bad_observations:
                        pos+=1
                        print('\033[92m'+"\t\t\t\t Doing gap fill for\t"+"year:\t"+str(y)+"\tday:\t"+str(d)+'\033[0m')
                        data[y][d] = set_gf(data[y][d],relation_dict,ini_good_obs,last_good_obs, len(bad_observations), pos,gf_key,"Yes")
                else:
                    print('\033[94m'+'\033[93m'+"\t\t\t part where the max obs > 4 i should leave them ****"+'\033[0m')
                    for (y,d) in bad_observations:
                        print("values left : gf i set to NA:\t"+"year:\t"+str(y)+"\tday:\t"+str(d))
                        data[y][d] = set_gf_no_gf(data[y][d],relation_dict,gf_key,"NA")
                # Fill good observation GF values
                print("\t\tyear:  "+str(year)+"day:  "+str(day)+"value: good_observation"+'\033[0m')
                data[year][day] = set_gf_no_gf(data[year][day],relation_dict,gf_key,"No")
                print("\t\tsetting/changing initial good obs to: "+"year:  "+str(year)+"day:  "+str(day)+"value: good_observation"+'\033[0m')
                ini_good_obs = data[year][day]
                #print("****good obs***:"+str(ini_good_obs)
                bad_observations=[]
    if len(bad_observations)>0:
        print("******************************************************************")
        print("now i looped through everything is still something left?")
        # Cannot gap fill because there is no good end value
        print(" i will leave those things and also tell you how many bad values exist that i don't want to deal with:"+str(len(bad_observations)))
        for (y,d) in bad_observations:
            print("\t\t filling bad_obs which cannot be fixed with NA:\t"+"year:\t"+str(y)+"day:\t"+str(d))
            data[y][d] = set_gf_no_gf(data[y][d],relation_dict,gf_key,"NA")
    return data
from modis import headers
def gap_fill(data,dataset):
    dataset = dataset.upper()
    print('\033[93m'+"*********************i entered gap fill code***********************"+'\033[0m')
    print(dataset)
    if dataset=='MOD09A1':
        print("data confirmed as mod09a1")
        gf_key='gf_applied'
        relation_dict = headers.get_gap_fill_relation_dict(dataset)
        print('\033[94m'+"******************this is relation_dict *********"+'\033[0m')
        print(relation_dict)
        is_bad_observation = mod09a1.is_bad_observation
        return gap_fill_algorithm(data,relation_dict,is_bad_observation,gf_key)
    else:
        return data

def __test__():
    pass