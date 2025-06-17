import requests
import json

def get_weather_data(city_name, unit_preference='imperial'):

    api_key = '30d4741c779ba94c470ca1f63045390a'

    units = "imperial" if unit_preference.lower() == 'imperial' else "metric"
    temp_unit_symbol = "ºF" if units == "imperial" else "ºC"

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'units': units,
        'APPID': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

        weather_data = response.json()

        if weather_data.get('cod') == '404':
            print(f"Error: No city found named '{city_name}'. Please check the spelling.")
            return None
        elif weather_data.get('cod') == '401':
            print("Error: Invalid API key. Please check your API key.")
            return None
        elif weather_data.get('cod') != 200:
            # Handle other potential API errors not specifically 404 or 401
            print(f"An unexpected API error occurred (code: {weather_data.get('cod')}).")
            return None
        else:
            return weather_data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} (Status Code: {response.status_code})")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}. Please check your internet connection.")
        return None
    except requests.exceptions.Timeout as timeout_err:
        print(f"Request timed out: {timeout_err}. The server took too long to respond.")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"An unknown error occurred during the request: {req_err}")
        return None
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response from the API.")
        print(f"Raw response content: {response.text}") # Print raw response for debugging
        return None

def display_weather_info(city_name, weather_data, unit_preference):
    """
    Displays formatted weather information from the weather_data dictionary.

    Args:
        city_name (str): The name of the city.
        weather_data (dict): The dictionary containing weather information.
        unit_preference (str): 'imperial' or 'metric' to display correct unit symbol.
    """
    if not weather_data:
        return # Exit if no valid weather data was provided

    # Extracting relevant information from the API response
    weather_description = weather_data['weather'][0]['description'].capitalize()
    main_weather = weather_data['weather'][0]['main']
    temperature = round(weather_data['main']['temp'])
    feels_like = round(weather_data['main']['feels_like'])
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    pressure = weather_data['main']['pressure']

    # Determine the correct unit symbols
    temp_unit_symbol = "ºF" if unit_preference.lower() == 'imperial' else "ºC"
    wind_speed_unit = "mph" if unit_preference.lower() == 'imperial' else "m/s"

    print(f"\n--- Current Weather in {city_name.title()} ---")
    print(f"Condition: {main_weather} ({weather_description})")
    print(f"Temperature: {temperature}{temp_unit_symbol} (Feels like: {feels_like}{temp_unit_symbol})")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} {wind_speed_unit}")
    print(f"Pressure: {pressure} hPa") # hPa is hectopascal, common unit for pressure

def main():
    """
    Main function to run the weather application.
    """
    while True:
        user_input_city = input("\nEnter city name (or 'exit' to quit): ").strip()
        if not user_input_city:
            print("City name cannot be empty. Please try again.")
            continue
        if user_input_city.lower() == 'exit':
            print("Exiting weather application. Goodbye!")
            break

        while True:
            unit_choice = input("Choose units (Imperial - F/mph or Metric - C/m/s)? [I/M]: ").strip().lower()
            if unit_choice in ['i', 'imperial']:
                selected_units = 'imperial'
                break
            elif unit_choice in ['m', 'metric']:
                selected_units = 'metric'
                break
            else:
                print("Invalid unit choice. Please enter 'I' for Imperial or 'M' for Metric.")

        print(f"Fetching weather data for {user_input_city}...")
        weather_data = get_weather_data(user_input_city, selected_units)

        if weather_data:
            display_weather_info(user_input_city, weather_data, selected_units)

if __name__ == "__main__":
    main()