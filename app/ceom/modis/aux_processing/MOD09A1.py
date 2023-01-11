
def process_MOD09A1(input_df):
    QC_COLUMNS = ['MODLAND QA', 'Band 1 Data Quality', 'Band 2 Data Quality', 'Band 3 Data Quality', 
                    'Band 4 Data Quality', 'Band 5 Data Quality', 'Band 6 Data Quality', 'Band 7 Data Quality', 
                    'Atmospheric Correction Performed', 'Adjacency Correction Performed']
    input_df[QC_COLUMNS] = input_df.apply(process_qc, axis=1, result_type='expand')
    input_df = input_df.drop('sur_refl_qc_500m', axis=1)

    STATE_COLUMNS = ['Cloud State', 'Cloud Shadow', 'Land/Water Flag', 'Aerosol Quantity', 'Cirrus Detected', 
                        'Internal Cloud Algorithm Flag', 'Internal Fire Algorithm Flag', 'MOD35 Snow/Ice Flag', 
                        'Pixel is Adjacent to Cloud', 'Salt Pan', 'Internal Snow Mask']
    input_df[STATE_COLUMNS] = input_df.apply(process_state, axis=1, result_type='expand')
    input_df = input_df.drop('sur_refl_state_500m', axis=1)

    COLUMN_RENAMES = {
        'sur_refl_b01':'Band 1 - Red (620-670 nm)',
        'sur_refl_b02':'Band 2 - NIR1 (841-876 nm)',
        'sur_refl_b03':'Band 3 - Blue (459-479 nm)',
        'sur_refl_b04':'Band 4 - Green (545-565 nm)',
        'sur_refl_b05':'Band 5 - NIR2 (1230-1250 nm)',
        'sur_refl_b06':'Band 6 - SWIR1 (1628-1652 nm)',
        'sur_refl_b07':'Band 7 - SWIR2 (2105-2155 nm)',
        'sur_refl_szen':'Solar Zenith Angle',
        'sur_refl_vzen':'View Zenith Angle',
        'sur_refl_raz':'Relative Azimuth Angle',
        'sur_refl_day_of_year':'Day of Year',
    }

    input_df.columns = [COLUMN_RENAMES.get(x, x) for x in input_df.columns]

    return input_df





# https://lpdaac.usgs.gov/documents/306/MOD09_User_Guide_V6.pdf  -  Page 21
def process_qc(row):
    bin_qc = format(row['sur_refl_qc_500m'], '#034b')[2:]

    MODLAND_DICT = {
        '00':'corrected product produced at ideal quality -- all bands',
        '01':'corrected product produced at less than ideal quality -- some or all bands',
        '10':'corrected product not produced due to cloud effects -- all bands',
        '11':'corrected product not produced for other reasons -- some or all bands, may be fill value (11) [Note that a value of (11) overrides a value of (01)].',
    }

    BAND_DICT = {
        '0000':'highest quality',
        '0111':'noisy detector',
        '1000':'dead detector, data interpolated in L1B',
        '1001':'solar zenith >= 86 degrees',
        '1010':'solar zenith >= 85 and < 86 degrees',
        '1011':'missing input',
        '1100':'internal constant used in place of climatological data for at least one atmospheric constant',
        '1101':'correction out of bounds, pixel constrained to extreme allowable value',
        '1110':'L1B data faulty',
        '1111':'not processed due to deep ocean or clouds',
    }

    BIN_DICT = {
        '1': 'yes',
        '0': 'no'
    }

    # Ranges don't match user guide due to their ranges starting from LSB and working up to MSB
    modland_dat = MODLAND_DICT[bin_qc[30:32]] 
    band1_dat = BAND_DICT[bin_qc[26:30]]
    band2_dat = BAND_DICT[bin_qc[22:26]]
    band3_dat = BAND_DICT[bin_qc[18:22]]
    band4_dat = BAND_DICT[bin_qc[14:18]]
    band5_dat = BAND_DICT[bin_qc[10:14]]
    band6_dat = BAND_DICT[bin_qc[6:10]]
    band7_dat = BAND_DICT[bin_qc[2:6]]
    atmospheric_corr_dat = BIN_DICT[bin_qc[1]]
    adjacency_corr_dat = BIN_DICT[bin_qc[0]]

    return modland_dat, band1_dat, band2_dat, band3_dat, band4_dat, band5_dat, band6_dat, band7_dat, atmospheric_corr_dat, adjacency_corr_dat



# https://lpdaac.usgs.gov/documents/306/MOD09_User_Guide_V6.pdf  -  Page 24
def process_state(row):
    bin_state = format(row['sur_refl_state_500m'], '#018b')[2:]

    CLOUD_STATE_DICT = {
        '00':'clear',
        '01':'cloudy',
        '10':'mixed',
        '11':'not set, assumed clear',
    }

    BIN_DICT = {
        '1': 'yes',
        '0': 'no'
    }

    LAND_WATER_DICT = {
        '000':'shallow ocean',
        '001':'land',
        '010':'ocean coastlines and lake shorelines',
        '011':'shallow inland water',
        '100':'ephemeral water',
        '101':'deep inland water',
        '110':'continental/moderate ocean',
        '111':'deep ocean'
    }

    AEROSOL_DICT = {
        '00':'climatology',
        '01':'low',
        '10':'average',
        '11':'high',
    }

    CIRRUS_DICT = {
        '00':'none',
        '01':'small',
        '10':'average',
        '11':'high',
    }

    CLOUD_FLAG_DICT = {
        '1': 'cloud',
        '0': 'no cloud'
    }

    FIRE_FLAG_DICT = {
        '1': 'fire',
        '0': 'no fire'
    }

    SNOW_MASK_DICT = {
        '1': 'snow',
        '0': 'no snow'
    }

    # Ranges don't match user guide due to their ranges starting from LSB and working up to MSB
    cloud_states_dat = CLOUD_STATE_DICT[bin_state[14:16]]
    cloud_shadow_dat = BIN_DICT[bin_state[13]]
    land_water_dat = LAND_WATER_DICT[bin_state[10:13]]
    aerosol_dat = AEROSOL_DICT[bin_state[8:10]]
    cirrus_dat = CIRRUS_DICT[bin_state[6:8]]
    cloud_flag_dat = CLOUD_FLAG_DICT[bin_state[5]]
    fire_flag_dat = FIRE_FLAG_DICT[bin_state[4]]
    snow_flag_dat = BIN_DICT[bin_state[3]]
    pixel_cloud_adjacent_dat = BIN_DICT[bin_state[2]]
    salt_pan_dat = BIN_DICT[bin_state[1]]
    snow_mask_dat = SNOW_MASK_DICT[bin_state[0]]

    return cloud_states_dat, cloud_shadow_dat, land_water_dat, aerosol_dat, cirrus_dat, cloud_flag_dat, fire_flag_dat, snow_flag_dat, pixel_cloud_adjacent_dat, salt_pan_dat, snow_mask_dat