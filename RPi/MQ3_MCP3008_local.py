import time
import board
import digitalio
import busio
import RPi.GPIO as GPIO
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin where the MQ3 digital output is connected
mq3_digital_pin = 17  # Connect MQ3 DOUT to GPIO17

# Set up the GPIO pin as an input
GPIO.setup(mq3_digital_pin, GPIO.IN)

# Setup SPI for MCP3008
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D8)
mcp = MCP3008(spi, cs)

# Create an analog input channel on pin 0 for the MQ3
mq3_analog_channel = AnalogIn(mcp, 1)

try:
    while True:
        # Read the digital output from the MQ3 sensor
        gas_detected = GPIO.input(mq3_digital_pin)

        # Read analog value from the MQ3 gas sensor
        analog_value = mq3_analog_channel.value  # This returns a value between 0 and 65535
        voltage = mq3_analog_channel.voltage  # Voltage level from the sensor

        # Prepare the message to be printed locally
        digital_data = "Gas detected!" if gas_detected else "No gas detected."
        analog_data = f"MQ3 Sensor Reading: {analog_value} (Voltage: {voltage:.2f}V)"

        # Print the data for local logging
        print(digital_data)
        print(analog_data)

        # Sleep for a short period before reading again
        time.sleep(5)

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    # Cleanup GPIO when the program is terminated
    GPIO.cleanup()
