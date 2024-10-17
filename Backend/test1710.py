import spidev
import time

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, CE0 (Chip Select 0)
spi.max_speed_hz = 1350000

# Function to read SPI data from MCP3008 channel (0 to 7)
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Function to convert data to voltage level
def convert_volts(data, places):
    volts = (data * 3.3) / 1023  # MCP3008 is a 10-bit ADC
    volts = round(volts, places)
    return volts

# Main loop
try:
    while True:
        # Read data from CH0 (where MQ2 is connected)
        gas_level = read_channel(0)
        gas_volts = convert_volts(gas_level, 2)
        
        print(f"Gas Level: {gas_level}, Gas Volts: {gas_volts}V")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped.")
