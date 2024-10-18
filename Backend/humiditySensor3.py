import Adafruit_DHT
import time

# Set sensor type: DHT11 or DHT22
sensor = Adafruit_DHT.DHT22  # For DHT11, change this to Adafruit_DHT.DHT11

# Set GPIO pin where the sensor is connected
pin = 4

try:
    while True:
        # Use read_retry to get a sensor reading (it will retry up to 15 times if there is an error)
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temperature is not None:
            print(f"Temp={temperature:.1f}C  Humidity={humidity:.1f}%")
        else:
            print("Failed to retrieve data from humidity sensor")
        
        # Wait 2 seconds before the next read
        time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped by user")
