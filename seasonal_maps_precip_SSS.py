# datasets
ERA = xr.open_dataset('/mnt/e/DD2/Python/MATLAB/data_stream-oper_stepType-accum.nc')
smos = xr.open_dataset('/mnt/e/DD2/Python/MATLAB/sss.nc')

precip_hourly = ERA['cp']
sss = smos['Sea_Surface_Salinity']

lat_precip = ERA['latitude']
lon_precip = ERA['longitude']
lat_sss = smos['latitude']
lon_sss = smos['longitude']

# === Convert hourly precip to daily ===
time_precip = ERA['valid_time']
if not np.issubdtype(time_precip.dtype, np.datetime64):
    time_precip = xr.conventions.times.decode_cf_datetime(time_precip, ERA['valid_time'].units)
precip_hourly = precip_hourly.assign_coords(time=time_precip)
precip_hourly = precip_hourly.sel(time=slice('2005-01-01', '2024-12-31'))
precip_daily = precip_hourly.resample(time='1D').sum()

# === Seasonal masks ===
months = precip_daily['time'].dt.month
djfm_mask = months.isin([12,1,2,3])
jjas_mask = months.isin([6,7,8,9])

# === Seasonal means ===
precip_jjas = precip_daily.sel(time=jjas_mask).mean(dim='time')
precip_djfm = precip_daily.sel(time=djfm_mask).mean(dim='time')

if 'time' in sss.dims:
    sss_jjas = sss.sel(time=sss['time.month'].isin([6,7,8,9])).mean(dim='time')
    sss_djfm = sss.sel(time=sss['time.month'].isin([12,1,2,3])).mean(dim='time')
else:
    raise ValueError("SMOS dataset does not have a 'time' dimension.")

# === Define levels ===
levels_sss = np.arange(np.floor(float(sss.min())), np.ceil(float(sss.max())) + 1, 0.2)
vmax_precip = np.nanmax([precip_jjas.max().values, precip_djfm.max().values])
levels_precip = np.linspace(0, np.ceil(vmax_precip), 50)

# === Draw maps ===
raw_seasonal_map(
    data1=sss_jjas, data2=sss_djfm,
    lon=lon_sss, lat=lat_sss,
    title1='JJAS Mean SSS', title2='DJFM Mean SSS',
    var_name='Sea Surface Salinity',
    cmap='viridis', levels=levels_sss, unit='psu',
    output_name='seasonal_sss_map.png'
)

raw_seasonal_map(
    data1=precip_jjas, data2=precip_djfm,
    lon=lon_precip, lat=lat_precip,
    title1='JJAS Mean Precipitation', title2='DJFM Mean Precipitation',
    var_name='Precipitation',
    cmap='Blues', levels=levels_precip, unit='kg m⁻² d⁻¹',
    output_name='seasonal_precip_map.png'
)
