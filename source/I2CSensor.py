from Sensor import Sensor
from abc import abstractmethod
import busio
import board


class I2CSensor(Sensor):
    def __init__(self, i2c_bus:busio.I2C):
        self._i2c_bus = i2c_bus

    @abstractmethod
    def readValue(self):
        pass
   