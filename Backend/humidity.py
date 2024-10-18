import Adafruit_DHT
import time

# Set the sensor type and GPIO pin
sensor = Adafruit_DHT.DHT11
pin = 4

while True:
    # Use read_retry to get a sensor reading with retries
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        print(f'Temp={temperature:.1f}°C  Humidity={humidity:.1f}%')
    else:
        print('Failed to get reading. Try again!')

    # Wait 2 seconds before taking the next reading
    time.sleep(2)
