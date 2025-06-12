import xarray as xr
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Author: Mr. EBOLO NKONGO Victor
# Project: Interannual Variation Analysis Using Hovmöller Diagrams
# -----------------------------------------------------------------------------

# Load generic model output dataset
data = xr.open_dataset('model_output.nc')

# Add 'month' for seasonal grouping
data["month"] = data["time"].dt.month

# Define seasons and their months
seasons = {
    "Winter": [12, 1, 2],
    "Spring": [3, 4, 5],
    "Summer": [6, 7, 8],
    "Autumn": [9, 10, 11]
}

# Define generic variables
variables = {
    "Var1": data["var1"],
    "Var2": data["var2"],
    "Var3": data["var3"],
    "Var4": data["var4"]
}

# Color scale limits for each variable and season (vmin, vmax)
vmin_max = {
    "Var1": {"Winter": (100, 200), "Spring": (110, 210), "Summer": (120, 220), "Autumn": (115, 215)},
    "Var2": {"Winter": (10, 30), "Spring": (15, 35), "Summer": (20, 40), "Autumn": (18, 38)},
    "Var3": {"Winter": (300, 400), "Spring": (310, 410), "Summer": (320, 420), "Autumn": (315, 415)},
    "Var4": {"Winter": (7.9, 8.1), "Spring": (7.85, 8.05), "Summer": (7.95, 8.15), "Autumn": (7.90, 8.10)}
}

def plot_hovmoller(var, label, months, season, ax, vmin, vmax):
    """
    Plot a Hovmöller diagram for the given variable and season.
    Zonal mean is calculated and displayed as filled contours over time and latitude.
    """
    seasonal_data = var.where(data["month"].isin(months), drop=True)
    zonal_mean = seasonal_data.mean(dim="longitude")

    contour = ax.contourf(
        zonal_mean["time"],
        zonal_mean["latitude"],
        zonal_mean.transpose(),
        cmap="jet",
        levels=100,
        vmin=vmin,
        vmax=vmax
    )
    ax.contour(
        zonal_mean["time"],
        zonal_mean["latitude"],
        zonal_mean.transpose(),
        colors='k',
        linewidths=0.5
    )
    
    ax.set_title(f"{season}", fontsize=14)
    ax.set_xlabel("Time")
    ax.set_ylabel("Latitude (°)")
    ax.grid(True)
    
    cbar = plt.colorbar(contour, ax=ax)
    cbar.set_label(label, fontsize=10)

# Create plot grid for 4 variables and 4 seasons
fig, axes = plt.subplots(4, 4, figsize=(18, 20))
axes = axes.reshape(4, 4)

for i, (var_label, var_data) in enumerate(variables.items()):
    for j, (season_name, months_list) in enumerate(seasons.items()):
        ax = axes[i, j]
        vmin, vmax = vmin_max[var_label][season_name]
        plot_hovmoller(var_data, var_label, months_list, season_name, ax, vmin, vmax)

plt.tight_layout()
plt.savefig("seasonal_hovmoller.png", dpi=300)
plt.show()
