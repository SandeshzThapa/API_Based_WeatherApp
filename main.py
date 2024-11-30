import requests
import pyttsx3
import json
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(filename='weather_app.log', level=logging.DEBUG)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def change_speech_properties():
    """Allow the user to change speech properties such as volume and voice."""
    print("\nChange Speech Properties:")
    print("1. Change volume")
    print("2. Change voice")
    
    choice = input("Choose an option (1 or 2): ").strip()
    
    if choice == "1":
        volume = float(input("Enter volume level (0.0 to 1.0): ").strip())
        engine.setProperty('volume', volume)
        print(f"Volume set to {volume}")
    
    elif choice == "2":
        voices = engine.getProperty('voices')
        print("\nAvailable Voices:")
        for i, voice in enumerate(voices, 1):
            print(f"{i}. {voice.name}")
        
        voice_choice = input("Choose a voice number: ").strip()
        if voice_choice.isdigit():
            voice_choice = int(voice_choice)
            if 1 <= voice_choice <= len(voices):
                engine.setProperty('voice', voices[voice_choice - 1].id)
                print(f"Voice set to {voices[voice_choice - 1].name}")
            else:
                print("Invalid choice. Please select a valid voice number.")
        else:
            print("Invalid input. Please enter a number.")
    
    else:
        print("Invalid choice. Please choose 1 or 2.")

def save_weather_info(info, city, unit):
    """Save the weather information to a text file."""
    filename = f"weather_info_{city}_{unit}.txt"
    with open(filename, 'w') as file:
        file.write(info)
    print(f"Weather information saved to {filename}")
    engine.say(f"Weather information saved to {filename}")
    engine.runAndWait()

def get_weather_info(city, unit='C'):
    """Get current weather information for the specified city."""
    url = f"https://api.weatherapi.com/v1/current.json?key=ae787ae3e27c4079b6e154730242011&q={city}&aqi=no"
    r = requests.get(url)

    if r.status_code == 200:
        try:
            wdic = json.loads(r.text)
            temp_c = wdic["current"]["temp_c"]
            temp_f = wdic["current"]["temp_f"]
            weather_desc = wdic["current"]["condition"]["text"]
            humidity = wdic["current"]["humidity"]
            wind_speed = wdic["current"]["wind_kph"]
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Handle unit conversion based on user choice
            if unit == 'F':
                temp = temp_f
                unit_label = "Fahrenheit"
            else:
                temp = temp_c
                unit_label = "Celsius"
            
            weather_info = (f"As of {current_time}, the current temperature in {city} is {temp} degrees {unit_label}. "
                            f"The weather is {weather_desc}. "
                            f"Humidity is {humidity}% and wind speed is {wind_speed} kph.")

            print(weather_info)
            engine.say(weather_info)
            engine.runAndWait()

            return weather_info
        
        except KeyError:
            error_message = "Could not fetch the weather information. Please try again."
            logging.error(f"Error retrieving weather data for {city}: {error_message}")
            print(error_message)
            engine.say(error_message)
            engine.runAndWait()
    else:
        error_message = f"Failed to retrieve weather data for {city}. Please try again."
        logging.error(f"API failure for {city}: {error_message}")
        print(error_message)
        engine.say(error_message)
        engine.runAndWait()


def get_weather_forecast(city, unit='C'):
    """Get the weather forecast for the next 3 days for the specified city."""
    url = f"https://api.weatherapi.com/v1/forecast.json?key=ae787ae3e27c4079b6e154730242011&q={city}&days=3&aqi=no&alerts=no"
    r = requests.get(url)

    if r.status_code == 200:
        try:
            wdic = json.loads(r.text)
            forecast_info = "Weather forecast:\n"
            for day in wdic["forecast"]["forecastday"]:
                date = day["date"]
                # Handle temperature unit conversion
                if unit == 'C':
                    temp_max = day["day"]["maxtemp_c"]
                    temp_min = day["day"]["mintemp_c"]
                else:
                    temp_max = day["day"]["maxtemp_f"]
                    temp_min = day["day"]["mintemp_f"]
                weather_desc = day["day"]["condition"]["text"]

                forecast_info += (f"Date: {date}, Max Temp: {temp_max}°{unit}, Min Temp: {temp_min}°{unit}, "
                                  f"Weather: {weather_desc}\n")

            print(forecast_info)
            engine.say(forecast_info)
            engine.runAndWait()

            return forecast_info
        
        except KeyError:
            error_message = "Could not fetch the weather forecast. Please try again."
            logging.error(f"Error retrieving forecast for {city}: {error_message}")
            print(error_message)
            engine.say(error_message)
            engine.runAndWait()
    else:
        error_message = f"Failed to retrieve forecast data for {city}. Please try again."
        logging.error(f"API failure for forecast of {city}: {error_message}")
        print(error_message)
        engine.say(error_message)
        engine.runAndWait()


def run_weather_app():
    """Main function to run the weather app with multiple queries."""
    while True:
        print("Welcome to weather app created by Sandesh Thapa")
        engine.say("Welcome to weather app created by Sandesh Thapa")
        engine.runAndWait()
        city = input("Enter the name of the city: ").strip()

        # Ensure correct unit choice (Celsius or Fahrenheit)
        while True:
            unit_choice = input("Choose unit for temperature (C for Celsius, F for Fahrenheit): ").strip().upper()
            if unit_choice in ['C', 'F']:
                break
            else:
                print("Invalid choice. Please choose either 'C' for Celsius or 'F' for Fahrenheit.")

        weather_info = get_weather_info(city, unit=unit_choice)
        
        # Ask user if they want to save the weather information
        save_choice = input("Would you like to save the weather information? (yes or no): ").strip().lower()
        if save_choice == "yes":
            save_weather_info(weather_info, city, unit_choice)
        
        forecast_choice = input("Do you want the 3-day weather forecast? (yes or no): ").strip().lower()
        if forecast_choice == "yes":
            get_weather_forecast(city, unit=unit_choice)
        
        # Ask if the user wants to exit the app
        exit_choice = input("Do you want to exit the app? (yes or no): ").strip().lower()
        if exit_choice == "yes":
            print("Thank you for using the weather app!")
            engine.say("Thank you for using the weather app!")
            engine.runAndWait()
            break  # Exit the loop and stop the app

        # Ask if the user wants to make another query
        another_query = input("Do you want to make another query? (yes or no): ").strip().lower()
        if another_query != "yes":
            print("Thank you for using the weather app!")
            engine.say("Thank you for using the weather app!")
            engine.runAndWait()
            break  # Exit the loop and stop the app

        change_speech_properties()

if __name__ == "__main__":
    run_weather_app()






