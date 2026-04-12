"""
Core Mathematical and Physics Formulas for Solar Panel Optimization
Author: Jayden Lin
Location: Shenzhen, China (Latitude 22.5 N)

This module contains the fundamental A-Level physics and math equations
needed to calculate the sun's position and the solar radiation received
by a tilted surface.
"""

import numpy as np
import pandas as pd

# Constants
LATITUDE_SHENZHEN = 22.5  # degrees North
SOLAR_CONSTANT = 1361     # W/m^2 (approximate radiation at top of atmosphere)
ATMOSPHERIC_TRANSMITTANCE = 0.7  # simplified assumption for clear sky

def get_day_of_year(month, day):
    """Convert month and day to day of the year (n)."""
    date = pd.Timestamp(year=2023, month=month, day=day) # Year doesn't matter much for non-leap
    return date.dayofyear

def solar_declination(n):
    """
    Calculate solar declination angle (delta) for a given day of the year (n).
    Formula: delta = 23.45 * sin(360/365 * (n - 81))
    Returns angle in degrees.
    """
    radians = np.radians((360 / 365.0) * (n - 81))
    return 23.45 * np.sin(radians)

def solar_elevation_angle(lat, declination, hour_angle):
    """
    Calculate the solar elevation angle (alpha).
    Formula: sin(alpha) = sin(lat)*sin(delta) + cos(lat)*cos(delta)*cos(H)
    """
    lat_rad = np.radians(lat)
    dec_rad = np.radians(declination)
    h_rad = np.radians(hour_angle)
    
    sin_alpha = np.sin(lat_rad)*np.sin(dec_rad) + np.cos(lat_rad)*np.cos(dec_rad)*np.cos(h_rad)
    # Ensure value is between -1 and 1
    sin_alpha = np.clip(sin_alpha, -1.0, 1.0)
    alpha = np.arcsin(sin_alpha)
    return np.degrees(alpha)

def solar_azimuth_angle(lat, declination, elevation, hour_angle):
    """
    Calculate the solar azimuth angle (gamma).
    Returns angle in degrees (0 is South, negative is East, positive is West).
    """
    lat_rad = np.radians(lat)
    dec_rad = np.radians(declination)
    elv_rad = np.radians(elevation)
    
    # Avoid division by zero
    if np.cos(elv_rad) == 0:
        return 0.0
        
    cos_gamma = (np.sin(elv_rad)*np.sin(lat_rad) - np.sin(dec_rad)) / (np.cos(elv_rad)*np.cos(lat_rad))
    cos_gamma = np.clip(cos_gamma, -1.0, 1.0)
    
    gamma = np.degrees(np.arccos(cos_gamma))
    if hour_angle < 0:
        gamma = -gamma
    return gamma

def incident_angle(elevation, azimuth, panel_tilt, panel_azimuth=0):
    """
    Calculate the angle of incidence (theta) between the sun's rays and the normal to the panel.
    panel_tilt: 0 is horizontal, 90 is vertical
    panel_azimuth: 0 is facing South (optimal for Northern Hemisphere)
    """
    elv_rad = np.radians(elevation)
    sun_az_rad = np.radians(azimuth)
    tilt_rad = np.radians(panel_tilt)
    pan_az_rad = np.radians(panel_azimuth)
    
    # Formula for angle of incidence on a tilted surface
    cos_theta = np.sin(elv_rad)*np.cos(tilt_rad) + \
                np.cos(elv_rad)*np.sin(tilt_rad)*np.cos(sun_az_rad - pan_az_rad)
                
    cos_theta = np.clip(cos_theta, 0.0, 1.0) # Angle cannot be > 90 deg for direct radiation
    return np.degrees(np.arccos(cos_theta))

def daily_radiation(lat, n, tilt, panel_azimuth=0):
    """
    Calculate the total direct daily radiation on a tilted surface.
    Integrates from sunrise to sunset.
    Returns energy in Wh/m^2
    """
    declination = solar_declination(n)
    
    # Calculate sunrise/sunset hour angles
    lat_rad = np.radians(lat)
    dec_rad = np.radians(declination)
    
    tan_lat = np.tan(lat_rad)
    tan_dec = np.tan(dec_rad)
    
    if -tan_lat * tan_dec >= 1:
        return 0.0 # Sun never rises (polar night)
    elif -tan_lat * tan_dec <= -1:
        sunset_hour = 180.0 # Sun never sets (midnight sun)
    else:
        sunset_hour = np.degrees(np.arccos(-tan_lat * tan_dec))
        
    total_radiation = 0
    # Integrate over the day (every 10 minutes = 2.5 degrees of hour angle)
    step = 2.5
    for h in np.arange(-sunset_hour, sunset_hour, step):
        elevation = solar_elevation_angle(lat, declination, h)
        if elevation > 0:
            azimuth = solar_azimuth_angle(lat, declination, elevation, h)
            theta = incident_angle(elevation, azimuth, tilt, panel_azimuth)
            
            if theta < 90:
                # Direct radiation intensity on the surface (simplified model)
                # I = I0 * transmittance^(1/sin(elevation)) * cos(theta)
                air_mass = 1 / np.sin(np.radians(elevation))
                intensity = SOLAR_CONSTANT * (ATMOSPHERIC_TRANSMITTANCE ** air_mass) * np.cos(np.radians(theta))
                
                # Multiply by time step in hours (step/15)
                total_radiation += intensity * (step / 15.0)
                
    return total_radiation
