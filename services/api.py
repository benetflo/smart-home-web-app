import requests
from dotenv import load_dotenv
import os
import json
import urllib.request

load_dotenv()

API_KEY_WEATHER = os.getenv('OPENWEATHER_API_KEY')
API_KEY_NEWS = os.getenv('GNEWS_API_KEY')

def get_weather_info(city):

	if city:
		url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_WEATHER}&units=metric&lang=sv'
		response = requests.get(url)
		if response.status_code == 200:
			weather_data = response.json()
		else:
			weather_data = {"error": "Could not get weather data"}
	return weather_data

def get_news_articles():

	url = f"https://gnews.io/api/v4/top-headlines?country=se&max=10&apikey={API_KEY_NEWS}"

	with urllib.request.urlopen(url) as response:
		data = json.loads(response.read().decode("utf-8"))
		articles = data["articles"]
		if articles:
			return articles
	return None

def get_news_info():
	articles = get_news_articles()
	news_list = []

	for i in range(len(articles)):
		news_item = {
			"title": articles[i]['title'],
			"url":  articles[i]['url']
		}
		news_list.append(news_item)
	return news_list

def parse_weather_data(city):
	data = get_weather_info(city)

	if data:
		temp = data['main']['temp']
		feels_like_temp = data['main']['feels_like']
		air_pressure = data['main']['pressure']
		humidity = data['main']['humidity']
		visibility = data.get('visibility') # in meters
		wind_speed = data['wind']['speed'] # overall speed
		wind_gust = data['wind'].get('gust') # temporary peaks
		weather_description = data['weather'][0]['description']

		return temp, feels_like_temp, air_pressure, humidity, visibility, wind_speed, wind_gust, weather_description

	else:
		return None
