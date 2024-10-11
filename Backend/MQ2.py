import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)  # Assuming D0 is connected to GPIO17

# Define the MQTT broker details
broker = "75a6d5883ba24aafa29b3f1f830f6464.s1.eu.hivemq.cloud"  # HiveMQ Cloud broker
port = 8883  # Secure MQTT port for TLS
topic = "test/raspberrypi/data"  # Topic to publish data to
username = "hivemq.webclient.1728458341347"  # HiveMQ Cloud username
password = "O7K!8S%?b2F&tXg6sDdv"  # HiveMQ Cloud password

# Define the callback functions for MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print("Data published.")

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

# Main loop for gas detection and publishing data
try:
    while True:
        # Read GPIO pin
        gas_detected = GPIO.input(17)
        
        # Data to send: convert boolean to string for MQTT message
        data = "Gas detected!" if gas_detected else "No gas detected."
        
        # Print the data for local logging
        print(data)
        
        # Publish data to the MQTT topic
        result = client.publish(topic, data)
        
        # Check if publish was successful
        status = result[0]
        if status == 0:
            print(f"Sent `{data}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        
        # Sleep before the next detection
        time.sleep(5)

# Handle script interruption (e.g., Ctrl+C)
except KeyboardInterrupt:
    print("Exiting...")

# Cleanup
finally:
    client.loop_stop()  # Stop the MQTT loop
    GPIO.cleanup()  # Clean up GPIO
