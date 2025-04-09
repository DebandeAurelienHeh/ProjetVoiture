from I2CSensor import I2CSensor
import busio
import board
import adafruit_ina219

class INASensor(I2CSensor):
    def __init__(self, i2c_bus:busio.I2C):
        super().__init__(i2c_bus)
        self.__sensor = adafruit_ina219.INA219(self._i2c_bus)

    def readValue(self) -> dict:
        """
        Return a dictionary with the values of the sensor.
        The dictionary contains:
        - shunt_voltage - The shunt voltage in volts.
        - bus_voltage - The bus voltage in volts.
        - current - The current in milliamps.
        """
        return {
            "BusVoltage" : self.__sensor.bus_voltage,
            "Shunt Voltage" : self.__sensor.shunt_voltage/1000,
            "Current" : self.__sensor.current
        }