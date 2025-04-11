from Sensor import Sensor
from abc import abstractmethod
import busio
import board

"""
Abstract class for I2C sensors.
This class defines the basic structure for I2C sensors.
"""
class I2CSensor(Sensor):
    def __init__(self, i2c_bus:busio.I2C):
        self._i2c_bus = i2c_bus

    @abstractmethod
    def readValue(self):
        pass
   