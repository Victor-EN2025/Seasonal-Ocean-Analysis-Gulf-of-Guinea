import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

def draw_seasonal_map(ax, data, lon, lat, title, units, cmap='Spectral_r', levels=None):
    """
    Trace une carte géographique d’un champ environnemental avec projection Cartopy.

    Paramètres
    ----------
    ax : matplotlib.axes._subplots.AxesSubplot
        L'axe sur lequel tracer la carte.
    data : 2D array-like (xr.DataArray ou np.ndarray)
        Les données environnementales à représenter (ex. salinité, précipitations).
    lon : 1D ou 2D array
        Longitudes correspondantes aux données.
    lat : 1D ou 2D array
        Latitudes correspondantes aux données.
    title : str
        Titre du sous-graphe.
    units : str
        Unité à afficher dans la barre de couleur.
    cmap : str, optional
        Palette de couleurs utilisée (par défaut 'Spectral_r').
    levels : array-like, optional
        Niveaux pour les contours. Si None, valeurs automatiques.

    Auteur
    ------
    Mr EBOLO NKONGO Victor  
    Institut des Sciences Halieutiques, Université de Douala (Cameroun)  
    Date de création : juin 2025
    """

    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_extent([lon.min(), lon.max(), lat.min(), lat.max()], crs=ccrs.PlateCarree())
    
    ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, facecolor='lightgray', zorder=0)
    
    contour = ax.contourf(
        lon, lat, data,
        levels=levels if levels is not None else 20,
        transform=ccrs.PlateCarree(),
        cmap=cmap,
        extend='both'
    )

    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', linestyle='--', alpha=0.5)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'fontsize': 8}
    gl.ylabel_style = {'fontsize': 8}

    cbar = plt.colorbar(contour, ax=ax, orientation='vertical', pad=0.04, shrink=0.8)
    cbar.set_label(units, fontsize=10)
