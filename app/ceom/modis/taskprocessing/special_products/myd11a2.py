from ceom.modis.taskprocessing import aux_functions
from ceom.modis.taskprocessing import band_names

def qa_flags(ii):
    aq = {'00':'LST produced - good quality',
          '01':'LST produced - other quality',
          '10':'LST not produced due to cloud effects',
          '11':'LST not produced for reasons other than cloud'
          }
    return aq[ii]

def dq_flags(ii):
    aq = {'00':'good data quality',
          '01':'other quality',
          '10':'TBD',
          '11':'TBD'
          }
    return aq[ii]

def emis_error_flag(ii):
    aq = {'00':'average emissivity error <= 0.01',
          '01':'average emissivity error <= 0.02',
          '10':'average emissivity error <= 0.04',
          '11':'average emissivity error > 0.04'
          }
    return aq[ii]

def lst_error_flag(ii):
    aq = {'00':'average LST error <= 1K',
          '01':'average LST error <= 2K',
          '10':'average LST error <= 3K',
          '11':'average LST error > 3K'
          }
    return aq[ii]

def decodeQC(qc_day, qc_night):
    day_b16 = aux_functions.denary2binary(qc_day)
    day_qa = qa_flags(day_b16[14:16])
    day_dq = dq_flags(day_b16[12:14])
    day_emis = emis_error_flag(day_b16[10:12])
    day_lst = lst_error_flag(day_b16[8:10])

    day_dict = {
        'QC_day_b': day_b16,
        'Q_day_qa': day_qa,
        'Q_day_dq': day_dq,
        'Q_day_emis_error_flag': day_emis,
        'Q_day_lst_error_flag': day_lst,
    }

    night_b16 = aux_functions.denary2binary(qc_night)
    night_qa = qa_flags(night_b16[14:16])
    night_dq = dq_flags(night_b16[12:14])
    night_emis = emis_error_flag(night_b16[10:12])
    night_lst = lst_error_flag(night_b16[8:10])

    night_dict = {
        'QC_night_b': night_b16,
        'Q_night_qa': night_qa,
        'Q_night_dq': night_dq,
        'Q_night_emis_error_flag': night_emis,
        'Q_night_lst_error_flag': night_lst,
    }

    return day_dict | night_dict

def get_special_products(data):
    qc_dict = decodeQC(data['QC_Day'], data['QC_Night'])
    data = dict(list(data.items())+list(qc_dict.items()))
    return data

def is_bad_observation(data):
    # Cloud bits are clear or not set (assume clear) and clud_shadow=0 (no)
    return (data['sur_refl_state_500m_b'][14:16] in ('01','10')  ) or data['sur_refl_state_500m_b'][13]=='1'
