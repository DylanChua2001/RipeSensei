import time
import board
import adafruit_dht

# Set the sensor type and GPIO pin
dhtDevice = adafruit_dht.DHT11(board.D4)  # GPIO4 (Physical Pin 7)

try:
    while True:
        try:
            # Read humidity and temperature
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            
            # Print the values
            if humidity is not None and temperature is not None:
                print(f"Temp: {temperature:.1f}C  Humidity: {humidity:.1f}%")
            else:
                print("Failed to retrieve data from the sensor")
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        
        # Wait before reading again
        time.sleep(2)

except KeyboardInterrupt:
    print("Program terminated.")

finally:
    dhtDevice.exit()
