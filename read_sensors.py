# This file is used to read from multiple sensors.
from miscellaneous.sensors import read_mq2, read_mq3, read_mq135

if __name__ == "__main__":
    read_mq2()
    read_mq3()
    read_mq135()
