import requests
from datetime import datetime
import json

"""
Typecasting
Exceptions
Lists
Tuples
Sets
Dictionaries
"""

# weather alerts (both saved locations and input cities)
# add new locations
# gui

class WeatherBitApi:
    """
    Send requests, parse current weather and weather forecast data
    """

    api_key = "392ce406022d466495def47cd729dd54"
    url = "https://api.weatherbit.io/v2.0/forecast/daily"

    def __init__(self, city : str = None):
        if city:
            self.city = city
        else:
            self.city = fetch_current_location()
        self.weather_info = self._send_request()

    def parse_current_weather(self) -> dict:
        """
        extract current weather data from self.weatherdata

        :return: parsed current weather data dict
        """
        response = self.weather_info
        parsed_dict = dict()

        parsed_dict['city_name'] = response['city_name']
        parsed_dict['country_code'] = response['country_code']
        parsed_dict['timezone'] = response['timezone']
        parsed_dict['temp'] = response['data'][0]['temp']
        parsed_dict['description'] = response['data'][0]['weather']['description']
        parsed_dict['icon'] = response['data'][0]['weather']['icon']
        parsed_dict['vis'] = response['data'][0]['vis']
        parsed_dict['clouds'] = response['data'][0]['clouds']
        parsed_dict['day'] = datetime.now().strftime('%A')
        parsed_dict['lat'] = response['lat']
        parsed_dict['lon'] = response['lon']
        parsed_dict['date'] = response['data'][0]['datetime']
        parsed_dict['maxtemp'] = response['data'][0]['app_max_temp']
        parsed_dict['mintemp'] = response['data'][0]['app_min_temp']

        return parsed_dict

    def parse_forecast_weather(self) -> list:
        """
        parse six days of weather data
        :return: dict forecast of next six days
        """
        response = self.weather_info

        forecast = list()

        for data in response['data'][1:]:
            forecast.append({'temp':data['temp'],
                             'date':data['valid_date'],
                             'description':data['weather']['description'],
                             'icon':data['weather']['icon']})

        return forecast

    def _send_request(self):
        """
        send requests to api, and update self.weather_data
        """
        print("Request Sent.....")
        response = None

        try:
            response = requests.get(
                self.url,
                params=[('key', self.api_key), ('city', self.city), ('days', 7)],
                timeout=(2,5)
            )

            if response.status_code != 200:
                print(response.json())
                print("Error:", response.json()['status_message'])
                raise Exception(response)

        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Request Timeout: {e}")
        except requests.exceptions.HTTPError as e:
            print(f"HttpError: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Oops. Some Unknown Error Occurred")

        return response.json()


def fetch_current_location():
    url = 'http://ipinfo.io/json'
    response = requests.get(url)
    return response.json()['city']
