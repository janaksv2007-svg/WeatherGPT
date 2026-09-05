import json
import matplotlib.pyplot as plt

# Read historical weather data
with open("chennai_weather.json", "r", encoding="utf-8") as file:
    weather_data = json.load(file)

months = list(weather_data["monthly"].keys())

max_temperatures = []
min_temperatures = []
rainfall = []

for month in months:
    max_temperatures.append(weather_data["monthly"][month]["max_temp"])
    min_temperatures.append(weather_data["monthly"][month]["min_temp"])
    rainfall.append(weather_data["monthly"][month]["rainfall"])

# Temperature graph
plt.figure(figsize=(10, 5))
plt.plot(months, max_temperatures, marker="o", label="Maximum Temperature")
plt.plot(months, min_temperatures, marker="o", label="Minimum Temperature")

plt.title("Chennai Historical Monthly Temperature")
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
plt.close()

# Rainfall graph
plt.figure(figsize=(10, 5))
plt.bar(months, rainfall)

plt.title("Chennai Historical Monthly Rainfall")
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.close()
