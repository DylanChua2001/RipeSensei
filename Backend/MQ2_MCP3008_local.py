# for local viewing

import time
import board
import digitalio
import busio
import RPi.GPIO as GPIO
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

# Pin Definitions
MQ2_SENSOR_PIN = 1  # Analog pin on the MCP3008
DIGITAL_PIN = 17    # Digital pin for the sensor (optional)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIGITAL_PIN, GPIO.IN)  # Assuming D0 is connected to GPIO17 for digital reading

# Setup SPI for MCP3008
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D8)
mcp = MCP3008(spi, cs)

# Create an analog input channel on pin 0 for the MQ-2
gas_sensor = AnalogIn(mcp, MQ2_SENSOR_PIN)

try:
    while True:
        # Read analog value from the MQ-2 gas sensor
        analog_value = gas_sensor.value  # This returns a value between 0 and 65535
        voltage = gas_sensor.voltage  # Voltage level from the sensor

        # Read digital value (optional)
        digital_value = GPIO.input(DIGITAL_PIN)

        # Print the data for local logging
        data = f"MQ-2 Sensor Reading: {analog_value} (Voltage: {voltage:.2f}V), Digital: {digital_value}"
        print(data)

        # Log to file
        with open("gas_sensor_log.txt", "a") as log_file:
            log_file.write(f"{time.ctime()} - {data}\n")

        # Sleep for 5 seconds before the next detection
        time.sleep(5)

# Handle script interruption (e.g., Ctrl+C)
except KeyboardInterrupt:
    print("Exiting...")

# Handle other exceptions
except Exception as e:
    print(f"Error occurred: {e}")

# Cleanup
finally:
    GPIO.cleanup()  # Clean up GPIO
