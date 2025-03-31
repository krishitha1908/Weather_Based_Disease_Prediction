import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# OpenWeatherMap API Key
API_KEY = '6b25fff73156bcfbd67f1115e96d2251'  # Replace with your OpenWeatherMap API Key

# Load Dataset
df = pd.read_csv('weather_disease_extended.csv')

# Features and Labels
X = df[['temperature', 'humidity', 'aqi']]
y = df[['dengue_probability', 'malaria_probability', 'respiratory_issues_probability', 
        'cold_flu_probability', 'pneumonia_probability']]

# Binarize the Labels (1 if probability > 0.5, else 0)
y = (y > 0.5).astype(int)

# Split the Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Models for Each Disease
models = {}
for disease in y.columns:
    print(f"\nTraining model for {disease}...")
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train[disease])
    models[disease] = model
    
    # Predictions and Evaluation
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test[disease], y_pred)
    print(f"Accuracy for {disease}: {accuracy * 100:.2f}%")
    print(classification_report(y_test[disease], y_pred))

# Function to Fetch Weather Data from API
def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        aqi = 100  # Placeholder as OpenWeatherMap doesn't provide AQI in this endpoint
        print(f"\nReal-Time Weather Data for {city}:")
        print(f"Temperature: {temperature} °C")
        print(f"Humidity: {humidity} %")
        print(f"AQI (Placeholder): {aqi}")
        return temperature, humidity, aqi
    else:
        print("Error fetching weather data. Please check the city name and try again.")
        return None

# Prediction Function
def predict_disease(temp, humidity, aqi):
    input_data = pd.DataFrame([[temp, humidity, aqi]], columns=['temperature', 'humidity', 'aqi'])
    predictions = {}
    for disease, model in models.items():
        predictions[disease] = model.predict(input_data)[0]
    return predictions

# Get User Input and Fetch Weather Data
city = input("\nEnter Location (City Name): ")
weather_data = fetch_weather_data(city)

if weather_data:
    temp, humidity, aqi = weather_data
    predictions = predict_disease(temp, humidity, aqi)
    
    print("\nDisease Predictions:")
    for disease, risk in predictions.items():
        print(f"{disease}: {'High Risk' if risk == 1 else 'Low Risk'}")
