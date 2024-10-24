import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Constants for MQ135
SPI_CLOCK_PIN = board.SCK
SPI_MISO_PIN = board.MISO
SPI_MOSI_PIN = board.MOSI
CHIP_SELECT_PIN = board.D5
ADC_CHANNEL = MCP.P2 # ADC analog channel 2

# Setup SPI bus and MCP3008
spi_bus = busio.SPI(clock=SPI_CLOCK_PIN, MISO=SPI_MISO_PIN, MOSI=SPI_MOSI_PIN)
chip_select = digitalio.DigitalInOut(CHIP_SELECT_PIN)
mcp = MCP.MCP3008(spi_bus, chip_select)
chan = AnalogIn(mcp, ADC_CHANNEL)

def read_mq135():
    while True:
        analog_value = chan.value
        voltage = chan.voltage
        gas_detected = "Gas Detected!" if analog_value > 300 else "No Gas Detected"
        print(f"MQ135 - Analog Value: {analog_value}, Voltage: {voltage:.2f}V, Status: {gas_detected}")
        time.sleep(1)

if __name__ == "__main__":
    read_mq135()