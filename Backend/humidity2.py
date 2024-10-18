import pigpio
import dht11

# Initialize GPIO
pi = pigpio.pi()

# Initialize DHT11 sensor
sensor = dht11.DHT11(pi, 4)  # GPIO pin 4

while True:
    # Get sensor reading
    result = sensor.read()

    if result.is_valid():
        print(f"Temp: {result.temperature}°C, Humidity: {result.humidity}%")
    else:
        print("Error getting sensor data")

    # Wait 2 seconds before taking the next reading
    pi.time_sleep(2)

# We import the pigpio and dht11 libraries. pigpio is a library for controlling GPIO pins on the Raspberry Pi, and dht11 is a library specifically for the DHT11 sensor.
# We initialize the pigpio library and create a DHT11 sensor object, passing in the pigpio instance and the GPIO pin number (4).
# In the main loop, we call the read() method on the sensor object to get the temperature and humidity readings.
# If the reading is valid, we print the temperature and humidity values. Otherwise, we print an error message.
# We wait 2 seconds before taking the next reading.
# To use this script, you'll need to install the pigpio and dht11 libraries first:

# Code

# sudo apt-get install pigpio
# sudo pip3 install dht11
# Make sure to replace the GPIO pin number (4) with the correct pin for your setup.
