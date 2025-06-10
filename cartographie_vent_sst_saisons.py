import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec

# --- Load wind data ---
Wind = xr.open_dataset("cmems_obs-wind_glo_phy_my_l3-metopa-ascat-des-0.25deg_P1D-i_multi-vars_10.88W-15.88E_15.88S-10.88N_2010-01-01-2021-11-15.nc")
u_wind = Wind['eastward_wind']
v_wind = Wind['northward_wind']
wind_speed = Wind['wind_speed']
lat_wind = Wind['latitude']
lon_wind = Wind['longitude']

# Define seasonal masks
jas_mask = (Wind['time'].dt.month >= 6) & (Wind['time'].dt.month <= 9)    # Monsoon (JJAS)
djfm_mask = (Wind['time'].dt.month == 12) | (Wind['time'].dt.month <= 3)  # Harmattan (DJFM)

# Seasonal means for wind components and speed
u_jas = u_wind.sel(time=jas_mask).mean(dim='time')
v_jas = v_wind.sel(time=jas_mask).mean(dim='time')
ws_jas = wind_speed.sel(time=jas_mask).mean(dim='time')

u_djfm = u_wind.sel(time=djfm_mask).mean(dim='time')
v_djfm = v_wind.sel(time=djfm_mask).mean(dim='time')
ws_djfm = wind_speed.sel(time=djfm_mask).mean(dim='time')

# Define contour levels for wind speed plots
vmin, vmax = 0, np.ceil(np.nanmax([ws_jas.max(), ws_djfm.max()]))
contour_levels = np.linspace(vmin, vmax, 100)

# --- Load Sea Surface Temperature (SST) data ---
OSTIA = xr.open_dataset('/mnt/e/DD2/Python/donnee/SST.nc')
sst = OSTIA['analysed_sst'] - 273.15  # Convert from Kelvin to Celsius
lat_sst = OSTIA['latitude']
lon_sst = OSTIA['longitude']

jas_mask_sst = (OSTIA['time'].dt.month >= 7) & (OSTIA['time'].dt.month <= 9)    # Monsoon (JAS)
djfm_mask_sst = (OSTIA['time'].dt.month == 12) | (OSTIA['time'].dt.month <= 3)  # Harmattan (DJFM)

# Seasonal mean SST
sst_mean_jas = sst.sel(time=jas_mask_sst).mean(dim='time')
sst_mean_djfm = sst.sel(time=djfm_mask_sst).mean(dim='time')

contour_levels_sst = np.linspace(15, 30, 100)

# --- Plot wind data for Harmattan (DJFM) and Monsoon (JAS) ---
fig = plt.figure(figsize=(14, 6))
gs = GridSpec(1, 3, width_ratios=[1, 1, 0.05], wspace=0.08, figure=fig)

# Harmattan wind speed and vectors
ax1 = fig.add_subplot(gs[0], projection=ccrs.PlateCarree())
cf1 = ax1.contourf(lon_wind, lat_wind, ws_djfm, levels=contour_levels, cmap='plasma', antialiased=True)
ax1.coastlines(resolution='10m', linewidth=0.8)
ax1.add_feature(cfeature.BORDERS, linewidth=0.5)
ax1.add_feature(cfeature.LAND, facecolor='lightgray')
ax1.set_title('A) Harmattan (DJFM)', fontweight='bold')

step = 5
scale_val = 150
q1 = ax1.quiver(
    lon_wind[::step], lat_wind[::step],
    u_djfm[::step, ::step], v_djfm[::step, ::step],
    ws_djfm[::step, ::step],
    scale=scale_val, pivot='middle',
    color='k', width=0.002, headwidth=4, headlength=4,
    edgecolor='k', linewidth=0.5,
    transform=ccrs.PlateCarree()
)
ax1.quiverkey(q1, X=0.85, Y=0.9, U=5, label='5 m/s', labelpos='E', coordinates='axes', color='k', fontproperties={'size': '10'})

# Monsoon wind speed and vectors
ax2 = fig.add_subplot(gs[1], projection=ccrs.PlateCarree())
cf2 = ax2.contourf(lon_wind, lat_wind, ws_jas, levels=contour_levels, cmap='plasma', antialiased=True)
ax2.coastlines(resolution='10m', linewidth=0.8)
ax2.add_feature(cfeature.BORDERS, linewidth=0.5)
ax2.add_feature(cfeature.LAND, facecolor='lightgray')
ax2.set_title('B) Monsoon (JAS)', fontweight='bold')

q2 = ax2.quiver(
    lon_wind[::step], lat_wind[::step],
    u_jas[::step, ::step], v_jas[::step, ::step],
    ws_jas[::step, ::step],
    scale=scale_val, pivot='middle',
    color='k', width=0.002, headwidth=4, headlength=4,
    edgecolor='k', linewidth=0.5,
    transform=ccrs.PlateCarree()
)
ax2.quiverkey(q2, X=0.85, Y=0.9, U=5, label='5 m/s', labelpos='E', coordinates='axes', color='k', fontproperties={'size': '10'})

# Format axes: ticks and labels
for ax in [ax1, ax2]:
    lon_min, lon_max = float(lon_wind.min()), float(lon_wind.max())
    lat_min, lat_max = float(lat_wind.min()), float(lat_wind.max())
    xticks = np.arange(np.floor(lon_min), np.ceil(lon_max) + 1, 5)
    yticks = np.arange(np.floor(lat_min), np.ceil(lat_max) + 1, 5)

    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    ax.set_xticklabels([f'{abs(int(t))}°E' if t >= 0 else f'{abs(int(t))}°W' for t in xticks])
    ax.set_yticklabels([f'{abs(int(t))}°N' if t >= 0 else f'{abs(int(t))}°S' for t in yticks])
    ax.set_xlabel('Longitude')

ax1.set_ylabel('Latitude')

# Add wind speed colorbar
cbar_ax = fig.add_subplot(gs[2])
cbar_ticks = np.arange(int(vmin), int(vmax) + 1, 2)
cbar = fig.colorbar(cf2, cax=cbar_ax, orientation='vertical', ticks=cbar_ticks)
cbar.set_label('Wind speed (m/s)')
cbar.ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))  # integer labels only
cbar.ax.tick_params(labelsize=10)

plt.tight_layout()
plt.savefig('wind_harmattan_monsoon.png', dpi=300, bbox_inches='tight')
plt.show()


# --- Plot SST data for Harmattan (DJFM) and Monsoon (JAS) ---
fig2 = plt.figure(figsize=(14, 6))
gs2 = GridSpec(1, 3, width_ratios=[1, 1, 0.05], wspace=0.08, figure=fig2)

# Harmattan SST
ax3 = fig2.add_subplot(gs2[0], projection=ccrs.PlateCarree())
cf3 = ax3.contourf(lon_sst, lat_sst, sst_mean_djfm, levels=contour_levels_sst, cmap='jet', antialiased=True)
ax3.coastlines(resolution='10m', linewidth=0.8)
ax3.add_feature(cfeature.BORDERS, linewidth=0.5)
ax3.add_feature(cfeature.LAND, facecolor='lightgray')
ax3.set_title('C) Harmattan SST (DJFM)', fontweight='bold')

# Monsoon SST
ax4 = fig2.add_subplot(gs2[1], projection=ccrs.PlateCarree())
cf4 = ax4.contourf(lon_sst, lat_sst, sst_mean_jas, levels=contour_levels_sst, cmap='jet', antialiased=True)
ax4.coastlines(resolution='10m', linewidth=0.8)
ax4.add_feature(cfeature.BORDERS, linewidth=0.5)
ax4.add_feature(cfeature.LAND, facecolor='lightgray')
ax4.set_title('D) Monsoon SST (JAS)', fontweight='bold')

# Format axes: ticks and labels
for ax in [ax3, ax4]:
    lon_min, lon_max = float(lon_sst.min()), float(lon_sst.max())
    lat_min, lat_max = float(lat_sst.min()), float(lat_sst.max())
    xticks = np.arange(np.floor(lon_min), np.ceil(lon_max) + 1, 5)
    yticks = np.arange(np.floor(lat_min), np.ceil(lat_max) + 1, 5)

    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    ax.set_xticklabels([f'{abs(int(t))}°E' if t >= 0 else f'{abs(int(t))}°W' for t in xticks])
    ax.set_yticklabels([f'{abs(int(t))}°N' if t >= 0 else f'{abs(int(t))}°S' for t in yticks])
    ax.set_xlabel('Longitude')

ax3.set_ylabel('Latitude')

# Add SST colorbar
cbar_ax2 = fig2.add_subplot(gs2[2])
cbar_ticks_sst = np.arange(15, 31, 2)
cbar2 = fig2.colorbar(cf4, cax=cbar_ax2, orientation='vertical', ticks=cbar_ticks_sst)
cbar2.set_label('Temperature (°C)')
cbar2.ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))  # integer
