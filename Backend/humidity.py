import time
import board
import adafruit_dht
import digitalio

# Set up the DHT11 sensor on GPIO4 (Physical Pin 7)
dhtDevice = adafruit_dht.DHT11(board.D4)

try:
    while True:
        try:
            # Read temperature and humidity from the sensor
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity

            # Print the values
            if temperature is not None and humidity is not None:
                print(f"Temp: {temperature:.1f}°C  Humidity: {humidity:.1f}%")
            else:
                print("Failed to retrieve data from the sensor")
        except RuntimeError as error:
            # Handle any runtime errors
            print(f"Error: {error.args[0]}")
        
        # Wait before reading again
        time.sleep(2)

except KeyboardInterrupt:
    print("Program terminated.")

finally:
    dhtDevice.exit()
