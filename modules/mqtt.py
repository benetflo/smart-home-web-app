import paho.mqtt.client as paho
import os
from dotenv import load_dotenv

load_dotenv()

BROKER_IP = os.getenv('BROKER_IP')
BROKER_PORT = int(os.getenv('BROKER_PORT'))

mqtt_client = None

def connect_to_mqtt_broker():

	global mqtt_client

	try:
		mqtt_client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

		result = mqtt_client.connect(BROKER_IP, BROKER_PORT)

		if result == 0:
			print("Connected to MQTT!")
			return 0
		else:
			print("Connect to MQTT failed!")
			return 1
	except Exception as e:
		print(f"Error occurred while trying to connect to MQTT: {e}")
		return 1

def on_message(client, userdata, message):
	print("on_message callback triggered!")
	print(f"Message received on topic {message.topic}: {message.payload.decode()}")

def sub_to_topic(topic):
	global mqtt_client

	mqtt_client.on_message = on_message
	mqtt_client.subscribe(topic,qos=1)
	mqtt_client.loop_start()
