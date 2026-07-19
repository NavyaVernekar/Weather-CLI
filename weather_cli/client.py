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
    def __init__(self,api_key,url):
        self.api_key = api_key
        self.url = url
        self.params = {
            "q" : None,
            "appid": self.api_key,
            "units": "metric"
        }

    def check_response_code(self,response):
        if response.status_code != 200:
            try:
                message = response.json().get('message', 'Reason Unknown')
            except (KeyError, requests.exceptions.JSONDecodeError):
                message = 'Reason Unknown'
            print(f"API request failed with status code {response.status_code}: {message}")        
            return False
        return True
    
    def get_weather(self,city):
        self.params["q"] = city
        try:
            response = requests.get(self.url,params=self.params,timeout=API_TIMEOUT)
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
    api_key,url = load_api_key()

    if not api_key or not url:
        print("API key or URL not found in .env file. Please check the .env file.")
        exit(1)

    client = WeatherClient(api_key,url)
    city = "pune"
    # print(client.get_weather(city) if client.get_weather(city) else "No data returned.")
    result = client.get_weather(city)
    print(result if result else "No data returned.")