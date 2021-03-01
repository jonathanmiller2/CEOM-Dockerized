from ceom.celeryq.modis.special_products import mod09a1
from ceom.celeryq.modis import band_names
def dataset_is_available(dataset):

    accepted_list = [
            'MOD09A1',
        ]
    if dataset.upper() in accepted_list:
        return True
    return False

# Calculates EVI, returns None if there is abnormal data
def process_evi(red, nir1, blue):
    denom = float((nir1+6*red-7.5*blue+10000))
    if (red == -28672) or (red<1) or (nir1<=1) or (blue<=1) or (denom==0):
        return None
    return  2.5*float(nir1-red)/denom

# Returns the normalized difference of two bands, the order matters.
def calc_nd(band1, band2):
    band1 = float(band1)
    band2 = float(band2)
    return (band2-band1)/float(band1+band2)

def get_surface_reflectace_products(red,nir1,nir2,blue,swir1,swir2,green):
    evi = process_evi(red, nir1,blue)
    lswi = calc_nd(swir1, nir1)
    lswi2105 = calc_nd(swir2, nir1)
    ndvi = calc_nd(red, nir1)
    ndwi1200 = calc_nd(nir2, nir1)
    ndsi = calc_nd( swir1,green)
    return {
        'evi': evi,
        'lswi': lswi,
        'lswi2105': lswi2105,
        'ndvi': ndvi,
        'ndwi1200': ndwi1200,
        'ndsi': ndsi
    }

def get_vegetation_indexes(dataset,data):
    bn = band_names.get_band_names(dataset)
    dataset = dataset.upper()
    if dataset=='MOD09A1':
        veg_indexes = get_surface_reflectace_products(
            data[bn['red']],
            data[bn['nir1']],
            data[bn['nir2']],
            data[bn['blue']],
            data[bn['swir1']],
            data[bn['swir2']],
            data[bn['green']])
        special_indexes = mod09a1.get_special_products(data)
        data = dict(list(data.items())+list(veg_indexes.items())+list(special_indexes.items()))
        return data
    return {}
      
