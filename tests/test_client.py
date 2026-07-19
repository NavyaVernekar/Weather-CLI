import pytest
import requests
from weather_cli.client import WeatherClient,load_api_key

#successful fetch
def test_successful_weather_fetch(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"weather" :[{"main":"clear"}],"main":{"temp":24}}
    mocker.patch("weather_cli.client.requests.get",return_value=mock_response)

    weather_client = WeatherClient("fake_key","https://fake-url.com")
    result = weather_client.get_weather("pune")
    assert result == {"weather" :[{"main":"clear"}],"main":{"temp":24}}

#city not found
def test_city_not_found(mocker):
    mock_response = mocker.Mock()
    mock_response.statuscode = 404
    mock_response.json.return_value ={"message":"city not found"}
    mocker.patch("weather_cli.client.requests.get",return_value=mock_response)

    weather_client = WeatherClient("fake_key","https://fake-url.com")
    result = weather_client.get_weather("doesnotexistcity")
    assert result == None

def test_timeout(mocker):
    mocker.patch("weather_cli.client.requests.get",side_effect=requests.exceptions.Timeout)

    weather_client = WeatherClient("fake_key","https://fake-url.com")
    result = weather_client.get_weather("pune")

    result == None

def test_connection_error(mocker):
    mocker.patch("weather_cli.client.requests.get",side_effect=requests.exceptions.ConnectionError)

    weather_client = WeatherClient("fake_key","https://fake-url.com")
    result = weather_client.get_weather("pune")

    result == None

def test_generic_request_exception(mocker):
    mocker.patch("weather_cli.client.requests.get",side_effect=requests.exceptions.RequestException("Unexpected Error"))

    weather_client = WeatherClient("fake_key","https://fake-url.com")
    result = weather_client.get_weather("pune")

    result == None

def test_malformed_json_response(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = requests.exceptions.JSONDecodeError("bad json","",0)
    mocker.patch("weather_cli.client.requests.get",return_value=mock_response)

    weather_client = WeatherClient("fake_key","https://fake-url.com")
    result = weather_client.get_weather("pune")

    result == None

def test_missing_api_key(monkeypatch,mocker):
    monkeypatch.delenv("WEATHER_API_KEY",raising=False)
    monkeypatch.delenv("URL",raising=False)
    mocker.patch("weather_cli.client.load_dotenv")
    from weather_cli.client import load_api_key
    api_key,url = load_api_key()

    assert api_key == None
    assert url == None

    