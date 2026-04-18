"""
Notebook 01: Solar Trajectory over Shenzhen
This script visualizes the sun's path and elevation angle throughout the year
in Shenzhen (Latitude 22.5 N).
"""

import sys
import os
sys.path.append(os.path.abspath('src'))
from solar_physics import *

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# ============================================================
# 1. Solar Declination over the year
# ============================================================
days = np.arange(1, 366)
decs = [solar_declination(d) for d in days]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(days, decs, lw=2, color='#e74c3c')
ax.axhline(0, color='gray', linestyle='--')
ax.axhline(23.45, color='orange', linestyle=':', label='Tropic of Cancer (23.45°)')
ax.axhline(-23.45, color='blue', linestyle=':', label='Tropic of Capricorn (-23.45°)')

# Add solstices and equinoxes
ax.axvline(80, color='green', alpha=0.3, label='Spring Equinox')
ax.axvline(172, color='red', alpha=0.3, label='Summer Solstice')
ax.axvline(264, color='orange', alpha=0.3, label='Autumn Equinox')
ax.axvline(355, color='blue', alpha=0.3, label='Winter Solstice')

ax.set_title("Solar Declination Angle Throughout the Year", fontsize=14)
ax.set_xlabel("Day of the Year")
ax.set_ylabel("Declination Angle (Degrees)")
ax.set_xlim(1, 365)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))

plt.tight_layout()
plt.savefig('figures/01_solar_declination.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: figures/01_solar_declination.png")

# ============================================================
# 2. Maximum Elevation Angle at Solar Noon in Shenzhen
# ============================================================
# At solar noon, hour angle = 0
noon_elevations = [solar_elevation_angle(LATITUDE_SHENZHEN, d, 0) for d in decs]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(days, noon_elevations, lw=2, color='#3498db')
ax.axhline(90, color='gray', linestyle='--')

ax.set_title("Maximum Solar Elevation Angle (Solar Noon) in Shenzhen (Lat 22.5° N)", fontsize=14)
ax.set_xlabel("Day of the Year")
ax.set_ylabel("Elevation Angle (Degrees)")
ax.set_ylim(0, 95)

# Add text annotation
summer_max = max(noon_elevations)
winter_min = min(noon_elevations)
ax.annotate(f'Summer Solstice: {summer_max:.1f}°', xy=(172, summer_max), xytext=(180, summer_max-5),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))
ax.annotate(f'Winter Solstice: {winter_min:.1f}°', xy=(355, winter_min), xytext=(300, winter_min+10),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))

plt.tight_layout()
plt.savefig('figures/01_noon_elevation.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: figures/01_noon_elevation.png")

# ============================================================
# 3. Solar Trajectory (Elevation vs Azimuth) for Key Days
# ============================================================
key_days = {
    'Winter Solstice (Dec 21)': 355,
    'Spring/Autumn Equinox': 80,
    'Summer Solstice (Jun 21)': 172
}

fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': 'polar'})

colors = ['#3498db', '#2ecc71', '#e74c3c']

for (label, day), color in zip(key_days.items(), colors):
    dec = solar_declination(day)
    
    azimuths_rad = []
    elevations_r = [] # Polar plot uses radius for distance from center. Center = 90 deg elevation
    
    # Calculate for daylight hours
    for h in np.arange(-120, 120, 2): # -8 hours to +8 hours from noon
        el = solar_elevation_angle(LATITUDE_SHENZHEN, dec, h)
        if el > 0:
            az = solar_azimuth_angle(LATITUDE_SHENZHEN, dec, el, h)
            # Convert Azimuth: North=0, East=90, South=180, West=270
            # Our formula: South=0, East=-90, West=90
            plot_az = np.radians(az + 180)
            
            azimuths_rad.append(plot_az)
            elevations_r.append(90 - el) # 90 is center (zenith), 0 is edge (horizon)
            
    ax.plot(azimuths_rad, elevations_r, label=label, color=color, lw=2)

ax.set_theta_zero_location('N')
ax.set_theta_direction(-1) # Clockwise
ax.set_rmax(90)
ax.set_rticks([0, 30, 60, 90])
ax.set_yticklabels(['90°', '60°', '30°', '0°']) # Elevation angles

ax.set_title("Sun Path Diagram for Shenzhen (Lat 22.5° N)", va='bottom', y=1.08, fontsize=14)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

plt.tight_layout()
plt.savefig('figures/01_sun_path_polar.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: figures/01_sun_path_polar.png")
