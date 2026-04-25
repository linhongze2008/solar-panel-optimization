"""
Notebook 02: Solar Panel Angle Optimization
Shenzhen (Lat 22.5 N)

This script calculates the total theoretical solar radiation received by a panel
at different tilt angles throughout the year, and finds the optimal angle.
"""

import sys
import os
sys.path.append(os.path.abspath('src'))
from solar_physics import *

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# ============================================================
# 1. Calculate Daily Radiation for Different Tilt Angles
# ============================================================
print("Calculating radiation over 365 days for angles 0° to 90°...")

days = np.arange(1, 366)
tilt_angles = np.arange(0, 91, 1) # 0 to 90 degrees

# Matrix to store results (rows: days, cols: tilt angles)
radiation_matrix = np.zeros((len(days), len(tilt_angles)))

for i, day in enumerate(days):
    for j, tilt in enumerate(tilt_angles):
        radiation_matrix[i, j] = daily_radiation(LATITUDE_SHENZHEN, day, tilt, panel_azimuth=0)

# Convert to DataFrame for easier handling
df_rad = pd.DataFrame(radiation_matrix, index=days, columns=tilt_angles)

# Calculate annual total for each angle
annual_totals = df_rad.sum(axis=0) / 1000  # Convert to kWh/m^2

# Find the absolute best fixed angle
best_angle = annual_totals.idxmax()
max_energy = annual_totals.max()

print(f"Optimal Fixed Angle for Shenzhen: {best_angle}°")
print(f"Maximum Annual Energy: {max_energy:.2f} kWh/m^2")

# ============================================================
# 2. Plot: Annual Total Energy vs Tilt Angle
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(annual_totals.index, annual_totals.values, lw=2, color='#e67e22')

# Highlight the maximum point
ax.plot(best_angle, max_energy, 'ro', markersize=8)
ax.annotate(f'Optimal Angle: {best_angle}°\n({max_energy:.1f} kWh/m²)', 
            xy=(best_angle, max_energy), xytext=(best_angle+5, max_energy-50),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))

# Reference points
ax.axvline(LATITUDE_SHENZHEN, color='gray', linestyle='--', alpha=0.5)
ax.text(LATITUDE_SHENZHEN+1, annual_totals.min(), 'Latitude (22.5°)', color='gray', rotation=90, va='bottom')

ax.set_title("Annual Total Solar Radiation by Panel Tilt Angle in Shenzhen", fontsize=14)
ax.set_xlabel("Panel Tilt Angle (Degrees from horizontal)")
ax.set_ylabel("Annual Total Radiation (kWh/m²)")
ax.set_xlim(0, 90)

plt.tight_layout()
plt.savefig('figures/02_annual_optimization.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: figures/02_annual_optimization.png")

# ============================================================
# 3. Plot: Heatmap of Radiation (Day of Year vs Tilt Angle)
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))

# Subsample matrix for clearer plotting (every 5 days, every 2 degrees)
plot_df = df_rad.iloc[::5, ::2] / 1000 # Convert daily to kWh

# Heatmap
cax = ax.imshow(plot_df.T, aspect='auto', origin='lower', cmap='YlOrRd',
                extent=[1, 365, 0, 90])

ax.set_title("Daily Solar Radiation Yield (kWh/m²) across the Year", fontsize=14)
ax.set_xlabel("Day of the Year")
ax.set_ylabel("Panel Tilt Angle (Degrees)")

# Add best path (seasonal optimization)
best_daily_angles = df_rad.idxmax(axis=1)
ax.plot(best_daily_angles.index, best_daily_angles.values, 'b--', lw=2, alpha=0.7, label='Optimal Daily Angle')

ax.legend(loc='lower right')
plt.colorbar(cax, label='Daily Radiation (kWh/m²)')

plt.tight_layout()
plt.savefig('figures/02_radiation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: figures/02_radiation_heatmap.png")

# ============================================================
# 4. Compare Strategies: Fixed vs Seasonal
# ============================================================
# Strategy 1: Fixed at Best Angle (22 deg)
energy_fixed = max_energy

# Strategy 2: Perfectly Seasonal (Change angle every day)
energy_perfect_tracking = df_rad.max(axis=1).sum() / 1000

# Strategy 3: 4 Seasons (Adjust 4 times a year)
# Spring (Mar-May): avg best angle ~15
# Summer (Jun-Aug): avg best angle ~0 (flat)
# Autumn (Sep-Nov): avg best angle ~30
# Winter (Dec-Feb): avg best angle ~45
df_rad['month'] = [pd.Timestamp(2023, 1, 1) + pd.Timedelta(days=i-1) for i in days]
df_rad['month'] = df_rad['month'].apply(lambda x: x.month)

energy_4seasons = 0
for day in days:
    m = df_rad.loc[day, 'month']
    if m in [3, 4, 5]: tilt = 15
    elif m in [6, 7, 8]: tilt = 0
    elif m in [9, 10, 11]: tilt = 30
    else: tilt = 45
    energy_4seasons += df_rad.loc[day, tilt] / 1000

print("\nEfficiency Comparison:")
print(f"1. Fixed Optimal Angle ({best_angle}°): {energy_fixed:.2f} kWh/m² (100%)")
print(f"2. Adjusted 4 times/year: {energy_4seasons:.2f} kWh/m² ({energy_4seasons/energy_fixed*100:.1f}%)")
print(f"3. Daily Perfect Tracking: {energy_perfect_tracking:.2f} kWh/m² ({energy_perfect_tracking/energy_fixed*100:.1f}%)")

# Bar chart
fig, ax = plt.subplots(figsize=(8, 5))
strategies = ['Fixed Angle\n(22°)', '4 Seasons\nAdjustment', 'Daily tracking\n(Perfect)']
energies = [energy_fixed, energy_4seasons, energy_perfect_tracking]
colors = ['#95a5a6', '#3498db', '#2ecc71']

bars = ax.bar(strategies, energies, color=colors)
ax.set_ylim(0, max(energies) * 1.1)
ax.set_ylabel("Annual Total Radiation (kWh/m²)")
ax.set_title("Comparison of Solar Tracking Strategies in Shenzhen", fontsize=14)

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 10,
            f'{yval:.1f}\n({yval/energy_fixed*100:.1f}%)', 
            ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('figures/02_strategy_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: figures/02_strategy_comparison.png")
