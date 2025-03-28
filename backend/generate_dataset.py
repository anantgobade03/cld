import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_flood_dataset(num_samples=1000, start_date="2010-01-01", end_date="2023-12-31"):
    """
    Generate a synthetic dataset for flood prediction with historical data.
    
    Parameters:
    - num_samples: Number of data points to generate
    - start_date: Starting date for the historical data
    - end_date: Ending date for the historical data
    
    Returns:
    - DataFrame with relevant flood prediction features
    """
    # Convert date strings to datetime objects
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Calculate the date range in days
    date_range = (end - start).days
    
    # Initialize lists to store data
    dates = []
    regions = ["Region_A", "Region_B", "Region_C", "Region_D", "Region_E"]
    region_list = []
    rainfall_24h = []  # mm
    rainfall_72h = []  # mm
    river_level = []   # meters
    soil_moisture = [] # percentage
    slope_gradient = []  # degrees
    vegetation_cover = []  # percentage
    urbanization = []  # percentage
    temp = []  # celsius
    snowmelt = []  # mm water equivalent
    reservoir_level = []  # percentage of capacity
    previous_floods = []  # binary 0/1 in last month
    flood_occurred = []  # target variable
    
    # Generate data points
    for _ in range(num_samples):
        # Random date within the specified range
        random_days = random.randint(0, date_range)
        date = start + timedelta(days=random_days)
        dates.append(date)
        
        # Region
        region = random.choice(regions)
        region_list.append(region)
        
        # Base parameters
        base_rainfall = max(0, np.random.normal(50, 30))
        rainfall_24h.append(round(base_rainfall, 1))
        
        # 72h rainfall is related to 24h but with some randomness
        rainfall_72h.append(round(base_rainfall * random.uniform(1.5, 3.0), 1))
        
        # River level is influenced by rainfall
        base_river = 1 + (base_rainfall / 100 * random.uniform(1, 3))
        river_level.append(round(base_river, 2))
        
        # Soil moisture (influenced by rainfall and season)
        # Higher in spring/winter, lower in summer
        month = date.month
        season_factor = 1.2 if month in [12, 1, 2, 3, 4] else 0.8
        moisture = min(100, max(10, base_rainfall / 5 * season_factor * random.uniform(0.8, 1.2)))
        soil_moisture.append(round(moisture, 1))
        
        # Slope gradient (fixed for a region)
        if region == "Region_A":
            slope = random.uniform(2, 5)
        elif region == "Region_B":
            slope = random.uniform(5, 10)
        elif region == "Region_C":
            slope = random.uniform(1, 3)
        elif region == "Region_D":
            slope = random.uniform(7, 15)
        else:  # Region_E
            slope = random.uniform(3, 8)
        slope_gradient.append(round(slope, 1))
        
        # Vegetation cover (fixed for a region with seasonal variation)
        base_vegetation = {"Region_A": 60, "Region_B": 40, "Region_C": 75, "Region_D": 30, "Region_E": 50}
        season_veg = 1.1 if month in [4, 5, 6, 7, 8, 9] else 0.9
        veg_cover = min(95, max(5, base_vegetation[region] * season_veg * random.uniform(0.9, 1.1)))
        vegetation_cover.append(round(veg_cover, 1))
        
        # Urbanization (fixed for a region)
        urban_rates = {"Region_A": 70, "Region_B": 40, "Region_C": 20, "Region_D": 90, "Region_E": 50}
        urban_rate = urban_rates[region] * random.uniform(0.95, 1.05)
        urbanization.append(round(urban_rate, 1))
        
        # Temperature (seasonal)
        if month in [12, 1, 2]:  # Winter
            base_temp = random.uniform(-5, 10)
        elif month in [3, 4, 5]:  # Spring
            base_temp = random.uniform(5, 20)
        elif month in [6, 7, 8]:  # Summer
            base_temp = random.uniform(15, 35)
        else:  # Fall
            base_temp = random.uniform(0, 25)
        temp.append(round(base_temp, 1))
        
        # Snowmelt (more in spring, influenced by temperature)
        if month in [3, 4, 5] and base_temp > 5:  # Spring with warm temperatures
            melt = random.uniform(0, 30) * (base_temp / 10)
        elif month in [6] and region in ["Region_B", "Region_D"]:  # Mountains with summer melt
            melt = random.uniform(0, 15) * (base_temp / 15)
        else:
            melt = 0
        snowmelt.append(round(melt, 1))
        
        # Reservoir level (influenced by rainfall and season)
        base_reservoir = 50 + (rainfall_72h[-1] / 10) - (5 if month in [6, 7, 8, 9] else -5)
        reservoir = min(100, max(10, base_reservoir * random.uniform(0.9, 1.1)))
        reservoir_level.append(round(reservoir, 1))
        
        # Previous floods (binary, more likely if there was heavy rain)
        prev_flood = 1 if (rainfall_72h[-1] > 120 and random.random() < 0.7) or random.random() < 0.05 else 0
        previous_floods.append(prev_flood)
        
        # Determining if flood occurred (our target variable)
        # Complex relationship based on multiple factors
        flood_prob = 0
        
        # Rainfall impact (major factor)
        if rainfall_24h[-1] > 100:
            flood_prob += 0.4
        elif rainfall_24h[-1] > 50:
            flood_prob += 0.2
        
        if rainfall_72h[-1] > 200:
            flood_prob += 0.4
        elif rainfall_72h[-1] > 120:
            flood_prob += 0.2
        
        # River level impact
        if river_level[-1] > 3.5:
            flood_prob += 0.3
        elif river_level[-1] > 2.5:
            flood_prob += 0.15
        
        # Soil moisture (saturated soil can't absorb more water)
        if soil_moisture[-1] > 80:
            flood_prob += 0.15
        elif soil_moisture[-1] > 60:
            flood_prob += 0.05
        
        # Slope impact (steeper slopes = faster runoff)
        if slope_gradient[-1] > 10:
            flood_prob += 0.1
        elif slope_gradient[-1] < 3:
            flood_prob -= 0.05  # Slight negative impact for flat areas
        
        # Vegetation (higher vegetation = better water retention)
        if vegetation_cover[-1] > 70:
            flood_prob -= 0.1
        elif vegetation_cover[-1] < 30:
            flood_prob += 0.1
        
        # Urbanization impact (more urban = more runoff)
        if urbanization[-1] > 70:
            flood_prob += 0.15
        elif urbanization[-1] > 50:
            flood_prob += 0.05
        
        # Snowmelt contribution
        if snowmelt[-1] > 20:
            flood_prob += 0.2
        elif snowmelt[-1] > 10:
            flood_prob += 0.1
        
        # Reservoir levels (high = less capacity to handle additional water)
        if reservoir_level[-1] > 90:
            flood_prob += 0.2
        elif reservoir_level[-1] > 75:
            flood_prob += 0.1
        
        # Previous floods indicate flood-prone areas
        if previous_floods[-1] == 1:
            flood_prob += 0.15
        
        # Add some randomness
        flood_prob += random.uniform(-0.1, 0.1)
        
        # Final determination
        flood = 1 if flood_prob > 0.5 or random.random() < flood_prob * 0.7 else 0
        flood_occurred.append(flood)
    
    # Create DataFrame
    data = {
        "date": dates,
        "region": region_list,
        "rainfall_24h": rainfall_24h,
        "rainfall_72h": rainfall_72h,
        "river_level": river_level,
        "soil_moisture": soil_moisture,
        "slope_gradient": slope_gradient,
        "vegetation_cover": vegetation_cover,
        "urbanization": urbanization,
        "temperature": temp,
        "snowmelt": snowmelt,
        "reservoir_level": reservoir_level,
        "previous_floods": previous_floods,
        "flood_occurred": flood_occurred
    }
    
    df = pd.DataFrame(data)
    
    # Add year, month, day columns for easier analysis
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    
    # Calculate flood probability as continuous value for potential regression models
    df["flood_probability"] = df.apply(lambda row: 
        (0.3 * (row["rainfall_24h"] / 150) + 
         0.3 * (row["rainfall_72h"] / 250) +
         0.1 * (row["river_level"] / 5) +
         0.05 * (row["soil_moisture"] / 100) -
         0.05 * (row["vegetation_cover"] / 100) +
         0.1 * (row["urbanization"] / 100) +
         0.05 * (row["snowmelt"] / 30) +
         0.05 * (row["reservoir_level"] / 100) +
         0.05 * row["previous_floods"]), axis=1
    )
    
    # Make sure the probability is between 0 and 1
    df["flood_probability"] = df["flood_probability"].clip(0, 1)
    
    return df

# Generate the dataset
np.random.seed(42)  # For reproducibility
random.seed(42)
flood_data = generate_flood_dataset(num_samples=3000)

# Save the dataset to a CSV file
flood_data.to_csv("flood_prediction_dataset.csv", index=False)

print(f"Dataset created with {len(flood_data)} samples.")
print(f"Flood events: {flood_data['flood_occurred'].sum()} ({flood_data['flood_occurred'].mean() * 100:.2f}%)")

# Display a sample of the data
print("\nSample of the dataset:")
print(flood_data.head())

# Show basic statistics
print("\nBasic statistics:")
print(flood_data.describe())