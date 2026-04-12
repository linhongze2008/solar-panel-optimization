# Solar Panel Angle Optimization for Shenzhen ☀️

## About This Project

This project uses mathematical modeling and physics principles to determine the optimal installation angle for solar panels in Shenzhen, China (Latitude 22.5° N). As an A-Level student studying Physics and Mathematics, I wanted to apply the concepts of trigonometry and solar radiation energy to a real-world renewable energy problem.

Following my previous project on air quality analysis (which highlighted the severe impact of fossil fuel emissions), this project explores a clean energy solution by maximizing the efficiency of solar power generation in my local city.

## Research Objectives

1. Model the sun's trajectory (declination and elevation angles) throughout the year for Shenzhen's specific latitude.
2. Calculate the theoretical solar radiation received by a solar panel at different tilt angles.
3. Determine the optimal fixed tilt angle for year-round energy maximization.
4. Compare the efficiency of a fixed-angle system versus a seasonally-adjusted system.

## Methodology

This project does not rely on machine learning. Instead, it is built upon fundamental physics and astronomy formulas:
- **Solar Declination Angle ($\delta$)**: Calculated using the day of the year.
- **Solar Elevation Angle ($\alpha$)**: Calculated using latitude, declination, and hour angle.
- **Incident Angle ($\theta$)**: The angle between the sun's rays and the normal to the solar panel's surface.
- **Radiation Energy**: Modeled as $I = I_0 \times \cos(\theta)$, where $I_0$ is the direct solar radiation.

The code simulates 365 days of the year, evaluating tilt angles from 0° (flat) to 90° (vertical) to find the maximum energy yield.

## Project Structure

```
├── src/
│   ├── solar_physics.py             # Core mathematical & physics formulas
├── notebooks/
│   ├── 01_solar_trajectory.ipynb    # Modeling the sun's path over Shenzhen
│   ├── 02_angle_optimization.ipynb  # Calculating the best tilt angles
├── figures/                         # Generated plots and visualizations
├── report/
│   └── project_report.pdf           # Full academic report
└── requirements.txt                 # Python dependencies
```

## Tools Used

- Python 3.x
- NumPy (for trigonometric calculations and array operations)
- Pandas (for structuring daily/monthly data)
- Matplotlib & Seaborn (for visualizing the results)

## Author

**Jayden Lin (林宏泽)**
A-Level Student (Mathematics, Physics, Chemistry)
Shenzhen Senior High School Group (深圳高级中学高中园)
