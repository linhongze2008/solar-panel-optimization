# Project Report: Solar Panel Angle Optimization for Shenzhen

**Author:** Jayden Lin (林宏泽)  
**School:** Shenzhen Senior High School Group (深圳高级中学高中园)  
**Date:** April 2026  
**Curriculum:** A-Level (Mathematics, Physics, Chemistry)

---

## 1. Abstract
As the global imperative to transition toward renewable energy intensifies, maximizing the efficiency of solar power generation at the local level is crucial. This independent research project utilizes mathematical modeling and astronomical physics to determine the optimal installation angle for solar panels in Shenzhen, China (Latitude 22.5° N). By simulating the sun's trajectory and the theoretical direct solar radiation over 365 days, the study concludes that a fixed south-facing solar panel in Shenzhen achieves maximum annual energy yield (2,071 kWh/m²) when tilted at 19°. Furthermore, the study compares this baseline with a seasonal-adjustment strategy, finding that manually adjusting the tilt angle four times a year yields a 5.4% increase in energy production, presenting a highly cost-effective alternative to expensive automated tracking systems.

## 2. Introduction
### 2.1 Background and Motivation
My previous research on air quality in the Greater Bay Area revealed the profound impact of fossil fuel combustion on local atmospheric pollution, particularly regarding secondary pollutants like ozone. This realization shifted my focus from merely analyzing environmental problems to exploring sustainable solutions. Solar energy is a highly viable alternative in subtropical regions like Shenzhen. However, the efficiency of a solar panel is heavily dependent on its orientation relative to the sun. In my A-Level Physics and Mathematics courses, I learned the principles of trigonometry and radiation energy. I initiated this project to apply these theoretical concepts to a practical engineering problem: How can we mathematically optimize solar panel angles in my city?

### 2.2 Objectives
1. To construct a mathematical model of the sun's daily and seasonal trajectory specifically for Shenzhen's latitude.
2. To calculate the theoretical incident solar radiation on a tilted surface across different angles (0° to 90°).
3. To determine the absolute optimal fixed tilt angle for maximum annual energy yield.
4. To evaluate the economic feasibility of seasonal manual adjustments versus automated tracking systems.

## 3. Methodology and Physics Model
Unlike empirical data analysis, this project relies on a deterministic physics model implemented in Python using NumPy and Pandas.

### 3.1 Solar Declination and Elevation
The position of the sun changes daily due to the Earth's axial tilt (23.45°). I modeled the solar declination angle ($\delta$) for any given day ($n$) using the standard astronomical approximation:
`δ = 23.45° × sin[(360/365) × (n - 81)]`

Using this, the solar elevation angle ($\alpha$) at any given hour angle ($H$) was calculated using the spherical trigonometry formula:
`sin(α) = sin(Latitude) × sin(δ) + cos(Latitude) × cos(δ) × cos(H)`

### 3.2 Radiation and Angle of Incidence
The energy a solar panel receives is proportional to the cosine of the angle of incidence ($\theta$) between the sun's rays and the normal to the panel's surface. 
The theoretical direct radiation intensity ($I$) was calculated by integrating over the daylight hours, accounting for atmospheric transmittance based on the air mass (distance light travels through the atmosphere).

## 4. Results and Analysis
### 4.1 Solar Trajectory in Shenzhen
Shenzhen is located just south of the Tropic of Cancer (22.5° N < 23.45° N). The model accurately reflected this geographical quirk: during the Summer Solstice, the sun actually passes slightly to the *north* of the zenith at solar noon. For the vast majority of the year, however, the sun remains in the southern sky.

*(See Figure: 01_sun_path_polar.png and 01_noon_elevation.png)*

### 4.2 The Optimal Fixed Angle
By simulating the total annual radiation for every tilt angle from 0° (horizontal) to 90° (vertical), the model identified a clear peak. The optimal fixed installation angle for a south-facing panel in Shenzhen is **19°**. 

This result aligns beautifully with the general engineering rule of thumb, which suggests that the optimal fixed angle is roughly equal to the local latitude minus a few degrees to favor the summer months when days are longer. At 19°, the theoretical maximum annual direct radiation is 2,071.22 kWh/m².

*(See Figure: 02_annual_optimization.png)*

### 4.3 Strategy Comparison
I then modeled three different installation strategies to compare their efficiencies:
1. **Fixed Angle (19°):** 2,071 kWh/m² (Baseline - 100%)
2. **4-Season Adjustment:** Changing the angle manually four times a year (Spring: 15°, Summer: 0°, Autumn: 30°, Winter: 45°). Yield: 2,183 kWh/m² (**105.4%**)
3. **Perfect Daily Tracking:** Simulating an expensive dual-axis automated solar tracker. Yield: 2,211 kWh/m² (**106.8%**)

*(See Figure: 02_strategy_comparison.png)*

## 5. Discussion and Reflections
The strategy comparison yielded the most practical insight of this project. While an automated daily tracking system provides the absolute maximum energy, it only offers a marginal 1.4% improvement over a simple manual seasonal adjustment strategy. Given the high capital and maintenance costs of motorized tracking systems, adjusting the panels manually four times a year is mathematically and economically the most efficient strategy for residential solar installations in Shenzhen.

**Model Limitations:** It is important to note that this model calculates *theoretical clear-sky direct radiation*. It does not account for diffuse radiation (scattered light on cloudy days) or Shenzhen's specific weather patterns, such as the summer monsoon season. If I were to expand this project, I would integrate the actual historical cloud-cover data from my first project to create a more robust, hybrid empirical-theoretical model.

## 6. Conclusion
This project successfully translated abstract A-Level Physics and Mathematics concepts into a functional engineering simulation. By determining the optimal solar panel angle for Shenzhen (19°) and proving the cost-effectiveness of seasonal adjustments, I learned how mathematical modeling can drive sustainable urban development. This experience has solidified my intention to pursue a multidisciplinary education, where I can continue to leverage computational models to solve real-world environmental challenges.