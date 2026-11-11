
from src.weather import get_weather

city = input("Enter city name: ")

try:
    weather = get_weather(city)

    print("\nAGRI NOVA - WEATHER REPORT")
    print("-------------------------")

    print("City:", weather["city"])
    print("Temperature:", weather["temperature"], "°C")
    print("Humidity:", weather["humidity"], "%")
    print("Condition:", weather["condition"])
    print("Wind Speed:", weather["wind_speed"], "m/s")
    print("Rainfall:", weather["rainfall"], "mm")

except Exception as e:
    print("Error:", e)
