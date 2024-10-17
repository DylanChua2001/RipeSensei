import time
import board
import digitalio
import busio
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)  # Assuming D0 is connected to GPIO17 (optional if you still want to use digital)

# Setup SPI for MCP3008
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D8)
mcp = MCP3008(spi, cs)

# Create an analog input channel on pin 0 for the MQ-2
gas_sensor = AnalogIn(mcp, MCP3008.P0)

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
        # Read analog value from the MQ-2 gas sensor
        analog_value = gas_sensor.value  # This returns a value between 0 and 65535
        voltage = gas_sensor.voltage  # Voltage level from the sensor

        # Format data to send via MQTT (send both raw and voltage values)
        data = f"MQ-2 Sensor Reading: {analog_value} (Voltage: {voltage:.2f}V)"
        
        # Print the data for local logging
        print(data)
        
        # Publish data to the MQTT topic
        result = client.publish(topic, data)
        
        # Check if publish was successful
        status = result[0]
        if status == 0:
            print(f"Sent {data} to topic {topic}")
        else:
            print(f"Failed to send message to topic {topic}")
        
        # Sleep for 5 seconds before the next detection
        time.sleep(5)

# Handle script interruption (e.g., Ctrl+C)
except KeyboardInterrupt:
    print("Exiting...")

# Cleanup
finally:
    client.loop_stop()  # Stop the MQTT loop
    GPIO.cleanup()  # Clean up GPIO