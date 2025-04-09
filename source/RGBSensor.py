from I2CSensor import I2CSensor
import adafruit_tcs34725
import busio
import board


class RGBSensor(I2CSensor):
    def __init__(self, i2c_bus:busio.I2C):
        super().__init__(i2c_bus)
        self.__sensor = adafruit_tcs34725.TCS34725(self._i2c_bus)
    
    def readValue(self):
        """ return a tuple with the values of the sensor Red Green Blue"""
        return self.__sensor.color_rgb_bytes
        