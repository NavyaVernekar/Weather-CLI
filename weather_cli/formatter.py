from client import WeatherClient

class WeatherInfo:
    def __init__(self,weather_data):
        self.weather_data = weather_data
        self.default = "No Information"

    
    def get_filtered_data(self, data):
        weather_list = data.get("weather") or [{}]
        raw = {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "weather_description": weather_list[0].get("description"),
            "temperature": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "humidity": data.get("main", {}).get("humidity"),
            "wind_speed": data.get("wind", {}).get("speed"),
        }
        return {k: (v if v is not None else self.default) for k, v in raw.items()}

    
    def display_weather_info(self):
        data = self.weather_data
        if not data :
            print("No weather data has been fetched; Please check logs for more information")
            return
        fil_data = self.get_filtered_data(data)

        print(f"{'-'*20}  City : {fil_data['city']} - Country : {fil_data['country']}  {'-'*20}")
        print(f"The weather currently is {fil_data['weather_description']}.")
        print(f"Temperature is {fil_data['temperature']} ; feels like {fil_data['feels_like']}.")
        print(f"Humidity : {fil_data['humidity']}")
        print(f"Wind speed : {fil_data['wind_speed']}")
        print(f"{'-'*70}")
    
if __name__ == "__main__":
    client = WeatherClient()
    city = "pune"
    # print(client.get_weather(city) if client.get_weather(city) else "No data returned.")
    result = client.get_weather(city)
    w = WeatherInfo(result)
    w.display_weather_info()
        