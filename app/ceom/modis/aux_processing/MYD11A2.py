# Column sorting happens in the tasks.py file. 
# This is because the sort depends on whether or not there is a "site" column,
# which depends on whether or not it's a single/multiple request.
MYD11A2_COLUMN_ORDER = [
    'Day 1km Grid Land Surface Temperature',
    'Daytime View Zenith Angle of Observation',
    'Daytime Time of Observation',
    'Night 1km Grid Land Surface Temperature ',
    'Nighttime View Zenith Angle of Observation',
    'Nighttime Time of Observation',
    'Band 31 Emissivity (10780 - 11280 nm)',
    'Band 32 Emissivity (11770 - 12270 nm)',
    'Days in Clear-Sky Conditions',
    'Nights in Clear-Sky Conditions',
    'Day QA Flag', 
    'Day Data Quality Flag', 
    'Day Terra/Aqua Combined-Use Flag', 
    'Day Emis Error Flag', 
    'Day LST Error Flag',
    'Night QA Flag', 
    'Night Data Quality Flag', 
    'Night Terra/Aqua Combined-Use Flag', 
    'Night Emis Error Flag', 
    'Night LST Error Flag'
]

def process_MYD11A2(input_df):
    DAY_QC_COLUMNS = ['Day QA Flag', 'Day Data Quality Flag', 'Day Terra/Aqua Combined-Use Flag', 'Day Emis Error Flag', 'Day LST Error Flag']
    input_df[DAY_QC_COLUMNS] = input_df.apply(process_qc, axis=1, result_type='expand', args=("QC_Day",))
    input_df = input_df.drop('QC_Day', axis=1)

    NIGHT_QC_COLUMNS = ['Night QA Flag', 'Night Data Quality Flag', 'Night Terra/Aqua Combined-Use Flag', 'Night Emis Error Flag', 'Night LST Error Flag']
    input_df[NIGHT_QC_COLUMNS] = input_df.apply(process_qc, axis=1, result_type='expand', args=("QC_Night",))
    input_df = input_df.drop('QC_Night', axis=1)

    COLUMN_RENAMES = {
        'Clear_sky_days':'Days in Clear-Sky Conditions',
        'Clear_sky_nights':'Nights in Clear-Sky Conditions',
        'Day_view_angl':'Daytime View Zenith Angle of Observation',
        'Day_view_time':'Daytime Time of Observation',
        'Emis_31':'Band 31 Emissivity (10780 - 11280 nm)',
        'Emis_32':'Band 32 Emissivity (11770 - 12270 nm)',
        'LST_Day_1km':'Day 1km Grid Land Surface Temperature',
        'LST_Night_1km':'Night 1km Grid Land Surface Temperature ',
        'Night_view_angl':'Nighttime View Zenith Angle of Observation',
        'Night_view_time':'Nighttime Time of Observation',
    }

    input_df.columns = [COLUMN_RENAMES.get(x, x) for x in input_df.columns]

    return input_df





# https://lpdaac.usgs.gov/documents/118/MOD11_User_Guide_V6.pdf  -  Page 25
def process_qc(row, column_name):
    bin_qc = format(row[column_name], '#010b')[2:]

    QA_DICT = {
        '00':'LST produced, good quality, not necessary to examine more detailed QA',
        '01':'LST produced, other quality, recommend examination of more detailed QA',
        '10':'LST not produced due to cloud effects',
        '11':'LST not produced primarily due to reasons other than cloud',
    }

    QUAL_DICT = {
        '0':'good data quality',
        '1':'other quality data',
    }

    COMBINED_DICT = {
        '0': 'no',
        '1': 'yes'
    }

    EMIS_DICT = {
        '00': 'average emissivity error <= 0.01',
        '01': 'average emissivity error <= 0.02',
        '10': 'average emissivity error <= 0.04',
        '11': 'average emissivity error > 0.04',
    }

    LST_DICT = {
        '00': 'average LST error <= 1K',
        '01': 'average LST error <= 2K',
        '10': 'average LST error <= 3K',
        '11': 'average LST error > 3K',
    }

    # Ranges don't match user guide due to their ranges starting from LSB and working up to MSB
    qa_dat = QA_DICT[bin_qc[6:8]] 
    qual_dat = QUAL_DICT[bin_qc[5]]
    combined_dat = COMBINED_DICT[bin_qc[4]]
    emis_dat = EMIS_DICT[bin_qc[2:4]]
    lst_dat = LST_DICT[bin_qc[0:2]]

    return qa_dat, qual_dat, combined_dat, emis_dat, lst_dat
