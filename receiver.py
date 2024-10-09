import paho.mqtt.client as mqtt

# Define the MQTT broker details
broker = "75a6d5883ba24aafa29b3f1f830f6464.s1.eu.hivemq.cloud"  # HiveMQ Cloud broker
port = 8883  # Secure MQTT port for TLS
topic = "test/raspberrypi/mq3data"  # Topic to subscribe to
username = "hivemq.webclient.1728458341347"  # HiveMQ Cloud username
password = "O7K!8S%?b2F&tXg6sDdv"  # HiveMQ Cloud password

# Define the callback function for when a message is received
def on_message(client, userdata, msg):
    # Print the received message
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

# Define the callback function for MQTT connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        # Subscribe to the topic once connected
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")
    else:
        print(f"Failed to connect, return code {rc}")

# Create an MQTT client instance
client = mqtt.Client("RaspberryPiSubscriber")

# Set callbacks for connect and message events
client.on_connect = on_connect
client.on_message = on_message

# Enable TLS for secure connection
client.tls_set()

# Set username and password for HiveMQ Cloud
client.username_pw_set(username, password)

# Connect to the broker
client.connect(broker, port)

# Start the MQTT loop
client.loop_forever()  # Keeps the script running to listen for messages
