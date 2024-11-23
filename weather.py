import openmeteo_requests
import requests_cache
from retry_requests import retry
import numpy

def weather_get():
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": 52.52,
		"longitude": 13.41,
		"hourly": "temperature_2m"
	}
	responses = openmeteo.weather_api(url, params=params)

	response=responses[0]

	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

	temperature = int(hourly_temperature_2m[0])

	if temperature <= 10:
		return "cold"
	elif temperature > 10 and temperature <= 20:
		return "normal"
	return "hot"