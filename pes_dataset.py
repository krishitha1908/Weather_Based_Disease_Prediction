import pandas as pd
import random
from datetime import datetime, timedelta

# Cities with Different Climates
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata"]

# Start Date (6 months back)
start_date = datetime.today() - timedelta(days=180)

# Generate Data for 6 Months
date_range = [start_date + timedelta(days=i) for i in range(181)]

# Function to Generate Weather Data
def generate_weather(city, date):
    # Simulate different climates for each city
    base_temp = {"Delhi": (5, 40), "Mumbai": (20, 35), "Chennai": (22, 38), "Bangalore": (15, 30), "Kolkata": (18, 37)}
    base_humidity = {"Delhi": (30, 80), "Mumbai": (60, 95), "Chennai": (50, 90), "Bangalore": (40, 85), "Kolkata": (55, 90)}
    base_precipitation = {"Delhi": (0, 10), "Mumbai": (0, 50), "Chennai": (0, 40), "Bangalore": (0, 20), "Kolkata": (0, 35)}
    
    temp = round(random.uniform(*base_temp[city]), 1)
    humidity = round(random.uniform(*base_humidity[city]), 1)
    aqi = random.randint(50, 300)
    precipitation = round(random.uniform(*base_precipitation[city]), 1)
        
    return {
        "date": date.date(),
        "city": city,
        "temperature": temp,
        "humidity": humidity,
        "aqi": aqi,
        "precipitation": precipitation  # Added Precipitation Field
    }

# Function to Assign Disease Risk Probability
def assign_disease_risks(weather):
    temp, humidity, aqi, precipitation = weather["temperature"], weather["humidity"], weather["aqi"], weather["precipitation"]

    return {
        "dengue_probability": round(random.uniform(0.7, 1) if humidity > 70 and precipitation > 10 else random.uniform(0.1, 0.4), 2),
        "malaria_probability": round(random.uniform(0.6, 1) if temp > 30 and precipitation > 5 else random.uniform(0.1, 0.3), 2),
        "respiratory_issues_probability": round(random.uniform(0.7, 1) if aqi > 150 else random.uniform(0.2, 0.5), 2),
        "cold_flu_probability": round(random.uniform(0.7, 1) if temp < 20 and humidity > 60 else random.uniform(0.1, 0.4), 2),
        "pneumonia_probability": round(random.uniform(0.7, 1) if temp < 10 and humidity > 70 else random.uniform(0.1, 0.3), 2)
    }

# Generate Data for All Cities
weather_data = []
for city in CITIES:
    for date in date_range:
        weather = generate_weather(city, date)
        disease_risks = assign_disease_risks(weather)
        weather.update(disease_risks)
        weather_data.append(weather)

# Convert to DataFrame
final_df = pd.DataFrame(weather_data)

# Save to CSV
final_df.to_csv("weather_disease_extended.csv", index=False)

print("Data generation completed and saved to weather_disease_extended.csv.")
