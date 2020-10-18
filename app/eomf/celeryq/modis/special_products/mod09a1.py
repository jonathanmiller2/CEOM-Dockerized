from eomf.celeryq.modis import aux_functions
from eomf.celeryq.modis import band_names

def mod35_cloud(ii):
    cloud={'00':'clear',
        '01':'cloudy',
        '10':'mixed',
        '11':'not set, assumed clear'
        }
    return cloud[ii]

def cloud_shadow(i):
    cloud_s = {'1':'yes',
            '0':'no'
            }
    return cloud_s[i]


def land_water(iii):
    lw = {'000':'shallow ocean',
          '001':'land',
          '010':'ocean coastlines and lake shorelines',
          '011':'shallow inland water',
          '100':'ephemeral water',
          '101':'deep inland water',
          '110':'continental/moderate ocean',
          '111':'deep ocean'
          }
    return lw[iii]

def aerosol_quality(ii):
    aq = {'00':'climatology',
          '01':'low',
          '10':'average',
          '11':'high'
          }
    return aq[ii]

def cirrus(ii):
    cs = {'00':'none',
          '01':'small',
          '10':'average',
          '11':'high'
          }
    return cs[ii]

def cloud_algorithm(i):
    ca = {'1':'cloud',
          '0':'no cloud'
          }
    return ca[i]

def fire_algorithm(i):
    fa = {'1':'fire',
          '0':'no fire'
          }
    return fa[i]

def snow_ice(i):
    si = {'1':'yes',
          '0':'no'
          }
    return si[i]

def pixel_adjacent_cloud(i):
    pac = {'1':'yes',
           '0':'no'
           }
    return pac[i]

def BRDF_correction(i):
    BRDF = {'1':'yes',
        '0':'no'
        }
    return BRDF[i]

def snow_algorithm(i):
    sa = {'1':'yes',
          '0':'no'
          }
    return sa[i]

def decodeQC(qc2):
    b16 = aux_functions.denary2binary(qc2)
    cloud = mod35_cloud(b16[14:16])
    cloud_s = cloud_shadow(b16[13])
    lw = land_water(b16[10:13])
    aq = aerosol_quality(b16[8:10])
    cs = cirrus(b16[6:8])
    ca = cloud_algorithm(b16[5])
    fa = fire_algorithm(b16[4])
    si = snow_ice(b16[3])
    pac = pixel_adjacent_cloud(b16[2])
    BRDF = BRDF_correction(b16[1])
    sa = snow_algorithm(b16[0])

    code_dict = {
        'sur_refl_state_500m_b': b16,
        'Q_cloud':cloud,
        'Q_cloud_shadow':cloud_s,
        'Q_lw':lw,
        'Q_aq':aq,
        'Q_cs':cs,
        'Q_ca':ca,
        'Q_fa':fa,
        'Q_si':si,
        'Q_pac':pac,
        'Q_BRDF':BRDF,
        'Q_sa':sa}

    return code_dict

def get_extra_fields(data):
  bands = band_names.get_band_names('mod09a1')
  return {
    'red': float(data[bands['red']])/10000,
    'nir': float(data[bands['nir1']])/10000,
    'blue': float(data[bands['blue']])/10000,
    'green': float(data[bands['green']])/10000,
    'nir2': float(data[bands['nir2']])/10000,
    'swir1': float(data[bands['swir1']])/10000,
    'swir2': float(data[bands['swir2']])/10000,
  }
def get_special_products(data):
    modis_qc = band_names.get_band_names('mod09a1')['state']
    qc_dict = decodeQC(data[modis_qc])
    extra = get_extra_fields(data)
    data = dict(list(data.items())+list(qc_dict.items())+list(extra.items()))
    return data

def is_bad_observation(data):
    # Cloud bits are clear or not set (assume clear) and clud_shadow=0 (no)
    return (data['sur_refl_state_500m_b'][14:16] in ('01','10')  ) or data['sur_refl_state_500m_b'][13]=='1'
