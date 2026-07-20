import requests
#loading the api key from .env file
from dotenv import load_dotenv
import json


API_TIMEOUT = 10  # seconds

def load_api_key():
    load_dotenv()
    import os
    api_key = os.getenv("WEATHER_API_KEY")
    url = os.getenv("URL")
    if not api_key or not url:
        print("API key or URL not found in .env file. Please check the .env file.")
        return None, None
    return api_key,url

class WeatherClient:
    def __init__(self, api_key=None, url=None):
        if api_key is None and url is None:
            loaded = load_api_key()
            if hasattr(loaded, "api_key") and hasattr(loaded, "url"):
                api_key, url = loaded.api_key, loaded.url
            else:
                api_key, url = None, None

        self.api_key = api_key
        self.url = url
        if not self.api_key or not self.url:
            raise ValueError("WeatherClient requires a valid API key and URL from .env")
        self.params = {"q": None, "appid": self.api_key, "units": "metric"}

    def check_response_code(self, response):
        status_code = getattr(response, "status_code", getattr(response, "statuscode", None))
        if status_code != 200:
            try:
                message = response.json().get("message", "Reason Unknown")
            except (AttributeError, KeyError, requests.exceptions.JSONDecodeError):
                message = "Reason Unknown"
            print(f"API request failed with status code {status_code}: {message}")
            return False
        return True

    def get_weather(self, city):
        self.params["q"] = city
        try:
            response = requests.get(self.url, params=self.params, timeout=API_TIMEOUT)
        except requests.exceptions.Timeout:
            print(f"API request timed out after {API_TIMEOUT} seconds.")
            return
        except requests.ConnectionError:
            print("API request failed due to a connection error.")
            return
        except requests.RequestException as e:
            print(f"An error occurred during the API request: {e}")
            return

        if not self.check_response_code(response):
            return None
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print("Received malformed JSON from the API.")
            return None
    
if __name__ == "__main__":
    # api_key,url = load_api_key()

    # if not api_key or not url:
    #     print("API key or URL not found in .env file. Please check the .env file.")
    #     exit(1)

    client = WeatherClient()
    city = "pune"
    # print(client.get_weather(city) if client.get_weather(city) else "No data returned.")
    result = client.get_weather(city)
    print(result if result else "No data returned.")