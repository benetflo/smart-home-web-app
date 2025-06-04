from flask import Flask, jsonify
from flask import render_template
from services.api import parse_weather_data
from modules.mqtt import connect_to_mqtt_broker, sub_to_topic, msg_queue

import threading
import time
import os


app = Flask(__name__)

# GLOBALS
cached_weather = None
last_fetch_time = 0
CACHE_DURATION  = 30 * 60
temp_sensor_value = None

@app.route("/")
def login():
	return render_template("login.html")


@app.route("/api/temp_sensor")
def temp_sensor_api():
	global temp_sensor_value

	if not msg_queue.empty():
		msg = msg_queue.get()
		temp_sensor_value = msg

	return jsonify(temp_sensor_value=temp_sensor_value or "N/A")


@app.route("/home")
def home():

	global cached_weather, last_fetch_time, temp_sensor_value

	if not msg_queue.empty():
		msg = msg_queue.get()
		temp_sensor_value = msg


	current_time = time.time()

	if not cached_weather or (current_time - last_fetch_time) > CACHE_DURATION:
		city = "Haninge"
		cached_weather = parse_weather_data(city)
		last_fetch_time = current_time

	temp, feels_like_temp, air_pressure, humidity, visibility, wind_speed, wind_gust, weather_description = cached_weather

	return render_template("home.html", temp=temp, feels_like_temp=feels_like_temp, air_pressure=air_pressure, humidity=humidity, visibility=visibility, wind_speed=wind_speed, wind_gust=wind_gust, weather_description=weather_description, temp_sensor_value=temp_sensor_value)






def start_mqtt():

	global temp_sensor

	connect_to_mqtt_broker()
	temp_sensor = sub_to_topic("sensor/temp")

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
	mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
	mqtt_thread.start()

if __name__ == "__main__":
	app.run(debug=True)
