import xarray as xr
import matplotlib.pyplot as plt

# Open NetCDF file
data = xr.open_dataset('sortie_model.nc')

# Add 'month' variable for seasonal filtering
data["month"] = data["time"].dt.month

# Define months for each season
monsoon_months = [6, 7, 8, 9]    # (Monsoon)
harmattan_months = [12, 1, 2,3]    #  (Harmattan)

# Variables to analyse with clearer naming
variables = {
    "TA-LIAR": data["LIAR"],    # Total alkalinity
    "DIC-M": data["DICV"],      # Dissolved inorganic carbon
    "pCO2": data["pco2"],      # Partial pressure of CO2
    "pH": data["ph"]            # pH level
}

# vmin and vmax values for each variable and season (for colour scale)
vmin_max_dict = {
    "TA-LIAR": {"Monsoon": (2200, 2350), "Harmattan": (2200, 2350)},
    "DIC-M": {"Monsoon": (1950, 2100), "Harmattan": (1950, 2100)},
    "pCO2": {"Monsoon": (360, 430), "Harmattan": (360, 430)},
    "pH": {"Monsoon": (8.01, 8.08), "Harmattan": (8.01, 8.08)}
}

def plot_hovmoller(var, name, months, season_name, ax, vmin, vmax):
    """
    Plot a Hovmöller diagram (time vs latitude) for a given variable
    and specific season, with filled contours and contour lines.
    """
    # Filter data for the season
    var_season = var.where(data["month"].isin(months), drop=True)
    
    # Average over longitude to obtain lat/time section
    var_lon_mean = var_season.mean(dim="longitude")
    
    # Plot filled contours
    c = ax.contourf(
        var_lon_mean["time"], var_lon_mean["latitude"],
        var_lon_mean.transpose(),
        cmap="jet", levels=100, vmin=vmin, vmax=vmax
    )
    
    # Add black contour lines
    ax.contour(var_lon_mean["time"], var_lon_mean["latitude"], var_lon_mean.transpose(), colours='k', linewidths=0.5)
    
    # Title, labels and grid
    ax.set_title(f"{season_name.capitalize()}", fontsize=16)
    ax.set_xlabel("Time", fontsize=14)
    ax.set_ylabel("Latitude (°)", fontsize=14)
    ax.grid(True)
    
    # Colour bar with label
    cbar = plt.colorbar(c, ax=ax)
    cbar.set_label(name, fontsize=12)
    
    return var_lon_mean

# Create a 4x2 figure for 4 variables x 2 seasons
fig, axes = plt.subplots(4, 2, figsize=(14, 20))

# Loop through each variable and season to plot
for i, (var_name, var) in enumerate(variables.items()):
    for j, (season_name, months) in enumerate([("Monsoon", monsoon_months), ("Harmattan", harmattan_months)]):
        ax = axes[i, j]
        vmin, vmax = vmin_max_dict[var_name][season_name]
        plot_hovmoller(var, var_name, months, season_name, ax, vmin, vmax)

plt.tight_layout()
plt.savefig("hovmoller_all_variables_with_seasons_large_font.png", dpi=300)
plt.show()
