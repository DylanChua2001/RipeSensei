import paho.mqtt.client as mqtt
import time
import spidev

# Setup SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0 (CE0)
spi.max_speed_hz = 1350000

# Function to read from MCP3008
def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

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

# Main loop for reading from MQ3 sensor and publishing raw data
try:
    while True:
        # Read from MCP3008 channel 0 (where MQ3 sensor is connected)
        adc_value = read_adc(0)  # Read the raw analog data
        
        # Print the raw data for local logging
        print(f"Raw ADC Value: {adc_value}")
        
        # Publish the raw data to the MQTT topic
        result = client.publish(topic, str(adc_value))  # Send raw data as string
        
        # Check if publish was successful
        status = result[0]
        if status == 0:
            print(f"Sent `{adc_value}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        
        # Sleep for 5 seconds before next read
        time.sleep(5)

# Handle script interruption (e.g., Ctrl+C)
except KeyboardInterrupt:
    print("Exiting...")

# Cleanup
finally:
    client.loop_stop()  # Stop the MQTT loop
    spi.close()  # Close the SPI connection
