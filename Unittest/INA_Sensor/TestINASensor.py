import unittest
from unittest.mock import MagicMock, patch
from classes.INASensor import INASensor

"""
test_inasensor.py

Unit tests for the INASensor class, which inherits from I2CSensor and uses the INA219 sensor via the I²C bus.

This test module verifies the following:
- Proper initialization of the sensor with a mocked I²C bus.
- Accurate reading of bus voltage, shunt voltage (converted to volts), and current via the readValue() method.
- Correct structure and content of the dictionary returned by readValue().

All hardware interactions (with adafruit_ina219.INA219) are mocked to ensure unit tests can run independently of physical devices.

"""

class TestINASensor(unittest.TestCase):

    @patch('classes.INASensor.adafruit_ina219.INA219')
    def setUp(self, mock_ina219_class):

        self.mock_i2c_bus = MagicMock()
        self.mock_sensor_instance = MagicMock()
        mock_ina219_class.return_value = self.mock_sensor_instance

        self.mock_sensor_instance.bus_voltage = 12.3
        self.mock_sensor_instance.shunt_voltage = 75.0  
        self.mock_sensor_instance.current = 1.5

        self.sensor = INASensor("0x40", self.mock_i2c_bus)

    def test_read_value_returns_correct_dict(self):
        expected_result = {
            "BusVolatage": 12.3,
            "Shunt Voltage": 0.075,
            "Current": 1.5
        }

        result = self.sensor.readValue()
        self.assertEqual(result, expected_result)

    def test_sensor_is_initialized_with_i2c_bus(self):
        self.sensor._INASensor__sensor.__class__.assert_called_with(self.mock_i2c_bus)

if __name__ == '__main__':
    unittest.main()
