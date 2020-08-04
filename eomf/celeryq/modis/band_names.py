MOD09A1 = {
    'red'  : 'sur_refl_b01',
    'nir1' : 'sur_refl_b02',
    'blue' : 'sur_refl_b03',
    'green': 'sur_refl_b04',
    'nir2' : 'sur_refl_b05',
    'swir1': 'sur_refl_b06',
    'swir2': 'sur_refl_b07',
    'state': 'sur_refl_state_500m',
    'qc'   : 'sur_refl_qc_500m',
    'doy'  : 'sur_refl_day_of_year',
    'szen' : 'sur_refl_szen',
    'vzen' : 'sur_refl_vzen',
    'raz'  : 'sur_refl_raz',
    } 

def get_band_names(dataset):
    dataset = dataset.lower()
    if dataset == 'mod09a1':
        return MOD09A1
    return None 