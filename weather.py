import tkinter as tk
from tkinter import messagebox
import requests

def get_weather(city=None):
    if not city:
        city = city_entry.get()
    
    if not city:
        messagebox.showerror("Error", "Please enter a city or use the current location option.")
        return
    
    api_key = "API-KEY"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    weather_data = response.json()

    # Debugging: print the whole response to see what it contains
    print("API response:", weather_data)

    if response.status_code == 200:
        if "main" in weather_data:
            main = weather_data["main"]
            wind = weather_data["wind"]
            weather_description = weather_data["weather"][0]["description"]

            temperature = main["temp"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            wind_speed = wind["speed"]

            temp_celsius = temperature - 273.15  # Convert from Kelvin to Celsius

            weather_info = f"City: {city}\n"
            weather_info += f"Temperature: {temp_celsius:.2f}°C\n"
            weather_info += f"Pressure: {pressure} hPa\n"
            weather_info += f"Humidity: {humidity}%\n"
            weather_info += f"Wind Speed: {wind_speed} m/s\n"
            weather_info += f"Description: {weather_description}"

            result_label.config(text=weather_info)
        else:
            messagebox.showerror("Error", "City Not Found or API Error")
    else:
        messagebox.showerror("Error", f"Failed to get weather data. Error code: {response.status_code}")

def use_current_location():
    try:
        response = requests.get('http://ipinfo.io')
        data = response.json()
        location = data['city']
        get_weather(city=location)
    except Exception as e:
        messagebox.showerror("Error", "Unable to get current location. Make sure you are connected to the internet.")
        print(e)

# Set up the main application window
app = tk.Tk()
app.title("Weather App")
app.geometry("400x400")

# City label and entry
city_label = tk.Label(app, text="Enter City:", font=('bold', 14))
city_label.pack(pady=10)

city_entry = tk.Entry(app, width=20, font=('bold', 14))
city_entry.pack(pady=10)

# Get Weather button
get_weather_button = tk.Button(app, text="Get Weather", command=get_weather, font=('bold', 14))
get_weather_button.pack(pady=10)

# Use Current Location button
current_location_button = tk.Button(app, text="Use Current Location", command=use_current_location, font=('bold', 14))
current_location_button.pack(pady=10)

# Result label
result_label = tk.Label(app, text="", font=('bold', 14))
result_label.pack(pady=20)

# Run the app
app.mainloop()
