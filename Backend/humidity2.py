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
