
MOD09A1_HEADER = [
    ("date",             "Date"),
    ("sur_refl_b01",     "Surface_reflectance_for_band_1"),
    ("sur_refl_b02",     "Surface_reflectance_for_band_2"),
    ("sur_refl_b03",     "Surface_reflectance_for_band_3"),
    ("sur_refl_b04",     "Surface_reflectance_for_band_4"),
    ("sur_refl_b05",     "Surface_reflectance_for_band_5"),
    ("sur_refl_b06",     "Surface_reflectance_for_band_6"),
    ("sur_refl_b07",     "Surface_reflectance_for_band_7"),
    ("sur_refl_qc_500m", "Surface_reflectance_500m_quality_control_flags"),
    ("sur_refl_szen",    "Solar_zenith"),
    ("sur_refl_vzen",    "View_zenith"),
    ("sur_refl_raz",     "Relative_azimuth"),
    ("sur_refl_state_500m","Surface_reflectance_500m_state_flags"),
    ("sur_refl_day_of_year","Surface_reflectance_day_of_year"),
    ("real_date",        "actual_date"),
]

MOD09A1_PRODUCTS_HEADER = [
    ('red', 'red'),
    ('nir', 'nir1'),
    ('blue', 'blue'),
    ('green', 'green'),
    ('nir2', 'nir2'),
    ('swir1', 'swir1'),
    ('swir2', 'swir2'),
    ('ndvi', 'NDVI'),
    ('evi', 'EVI'),
    ('lswi', 'LSWI'),
    ('lswi2105', 'LSWI2105'),
    ('ndsi', 'NDSI'),
    ('ndwi1200', 'NDWI1200'),
    ('sur_refl_state_500m_b', 'sur_refl_state_500m (binary)'),
    ('Q_cloud', 'MOD35 cloud'),
    ('Q_cloud_shadow', 'cloud shadow'),
    ('Q_lw', 'land/water flag'),
    ('Q_aq', 'aerosol quantity'),
    ('Q_cs', 'cirrus detected'),
    ('Q_ca', 'internal cloud algorithm flag'),
    ('Q_fa', 'internal fire algorithm flag'),
    ('Q_si', 'MOD35 snow/ice flag'),
    ('Q_pac', 'Pixel is adjacent to cloud'),
    ('Q_BRDF', 'BRDF correction performed'),
    ('Q_sa', 'internal snow algorithm flag'),
    ('bad_obs', 'Bad observation'),
    ('gf_applied', 'Gap_fill_applied'),
    ('gf_ndvi', 'GF_NDVI'),
    ('gf_evi', 'GF_EVI'),
    ('gf_lswi', 'GF_LSWI'),
    ('gf_lswi2105', 'GF_LSWI2105 '),
    ('gf_ndsi', 'GF_NDSI'),
    ('gf_ndwi1200', 'GF_NDWI1200')
]
MOD09A1_GF_RELATION= [
    ('ndvi', 'gf_ndvi'),
    ('evi', 'gf_evi'),
    ('lswi', 'gf_lswi'),
    ('lswi2105', 'gf_lswi2105'),
    ('ndsi', 'gf_ndsi'),
    ('ndwi1200', 'gf_ndwi1200')
]

MYD11A2_HEADER = [
    ("date", "Date"),
    ("real_date", "Real Date"),
    ('LST_Day_1km', 'LST_Day_1km'),
    ('QC_Day', 'QC_Day'),
    ('Day_view_time', 'Day_view_time'),
    ('Day_view_angl', 'Day_view_angl'),
    ('LST_Night_1km', 'LST_Night_1km'),
    ('QC_Night', 'QC_Night'),
    ('Night_view_time', 'Night_view_time'),
    ('Night_view_angl', 'Night_view_angl'),
    ('Emis_31', 'Emis_31'),
    ('Emis_32', 'Emis_32'),
    ('Clear_sky_days', 'Clear_sky_days'),
    ('Clear_sky_nights', 'Clear_sky_nights'),
    ('QC_day_b', 'QC_day_b'),
    ('Q_day_qa', 'Q_day_qa'),
    ('Q_day_dq', 'Q_day_dq'),
    ('Q_day_emis_error_flag', 'Q_day_emis_error_flag'),
    ('Q_day_lst_error_flag', 'Q_day_lst_error_flag'),
    ('QC_night_b', 'QC_night_b'),
    ('Q_night_qa', 'Q_night_qa'),
    ('Q_night_dq', 'Q_night_dq'),
    ('Q_night_emis_error_flag', 'Q_night_emis_error_flag'),
    ('Q_night_lst_error_flag', 'Q_night_lst_error_flag'),
]

def get_modis_header(dataset, products=False):
    dataset = dataset.upper()
    if dataset=="MOD09A1":
        if not products:
            return MOD09A1_HEADER
        else:
            return MOD09A1_HEADER + MOD09A1_PRODUCTS_HEADER
    elif dataset=="MYD11A2":
        return MYD11A2_HEADER
    return []

def get_gap_fill_relation_dict(dataset):
    dataset = dataset.upper()
    if dataset=="MOD09A1":
        return MOD09A1_GF_RELATION
    elif dataset=="MYD11A2":
        return []
    return []
