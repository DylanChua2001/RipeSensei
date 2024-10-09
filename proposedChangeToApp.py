import paho.mqtt.client as mqtt
import time

import RPi.GPIO as GPIO
import time

# set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN) # Assuming D0 is connected to GPIO17

try:
	while True:
		gas_detected = GPIO.input(17)
		data = gas_detected
		
		if gas_detected:
			print("Gas detected!")
		else:
			print("No gas detected.")
		time.sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()


# Define the MQTT broker details
broker = "75a6d5883ba24aafa29b3f1f830f6464.s1.eu.hivemq.cloud"  # HiveMQ Cloud broker
port = 8883                   # Secure MQTT port for TLS
topic = "test/raspberrypi/data"  # Topic to publish data to
username = "hivemq.webclient.1728458341347"      # HiveMQ Cloud username
password = "O7K!8S%?b2F&tXg6sDdv"      # HiveMQ Cloud password

# Data to send
# data = "Hello from Raspberry Pi"

# Define the callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print('Failed to connect, return code', rc)

def on_publish(client, userdata, mid):
    print("Data published:", data)

# Create an MQTT client instance
client = mqtt.Client("RaspberryPiPublisher")

# Assign the callbacks
client.on_connect = on_connect
client.on_publish = on_publish

# Enable TLS for secure connection
client.tls_set()

# Set username and password for HiveMQ Cloud
client.username_pw_set(username, password)

# Connect to the broker
client.connect(broker, port)

# Start the MQTT loop in a background thread
client.loop_start()

# Publish the data
while True:
    result = client.publish(topic, data)
    
    # Check if publish was successful
    status = result[0]
    if status == 0:
        print("Sent", data," to topic ", topic)
    else:
        print("Failed to send message to topic ", topic)
    
    # Sleep for 5 seconds before sending next message
    time.sleep(5)

