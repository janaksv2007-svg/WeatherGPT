import json

# Read historical weather data
with open("chennai_weather.json", "r", encoding="utf-8") as file:
    weather_data = json.load(file)

# Historical monthly maximum temperatures
max_temperatures = []

for month in weather_data["monthly"]:
    max_temperatures.append(
        weather_data["monthly"][month]["max_temp"]
    )

# Calculate historical average maximum temperature
average_max_temp = sum(max_temperatures) / len(max_temperatures)

print("Historical Average Maximum Temperature:",
      round(average_max_temp, 2), "°C")
