import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin where the MQ3 digital output is connected
mq3_digital_pin = 17  # Connect MQ3 DOUT to GPIO17

# Set up the GPIO pin as an input
GPIO.setup(mq3_digital_pin, GPIO.IN)

# Define the MQTT broker details
broker = "75a6d5883ba24aafa29b3f1f830f6464.s1.eu.hivemq.cloud"  # HiveMQ Cloud broker
port = 8883  # Secure MQTT port for TLS
topic = "test/raspberrypi/mq3data"  # Topic to publish data to
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

try:
    while True:
        # Read the digital output from the MQ3 sensor
        gas_detected = GPIO.input(mq3_digital_pin)
        
        # Prepare the message to be sent over MQTT
        data = "Gas detected!" if gas_detected else "No gas detected."

        # Print the data for local logging
        print(data)
        
        # Publish the data to the MQTT topic
        result = client.publish(topic, data)
        
        # Check if publish was successful
        status = result[0]
        if status == 0:
            print(f"Sent `{data}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        
        # Sleep for a short period before reading again
        time.sleep(5)

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    # Cleanup GPIO and MQTT loop when the program is terminated
    GPIO.cleanup()
    client.loop_stop()  # Stop the MQTT loop
    client.disconnect()  # Disconnect from the broker
