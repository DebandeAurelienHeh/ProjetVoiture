import unittest
from unittest.mock import MagicMock
from sensors import LineSensor
from sensormanager import SensorManager

class TestDetectLineFromSensorManager(unittest.TestCase):

    def setUp(self):
        self.mock_sensor = MagicMock(spec=LineSensor)
        self.manager = SensorManager(lineSensor=self.mock_sensor)

    def test_detect_line_return_true_on_0(self):
        self.mock_sensor.readValue.return_value = 0
        result = self.manager.detectLine()
        self.assertTrue(result, "detectLine() doit retourner True si readValue() == 0")

    def test_detect_line_return_false_on_1(self):
        self.mock_sensor.readValue.return_value = 1
        result = self.manager.detectLine()
        self.assertFalse(result, "detectLine() doit retourner False si readValue() == 1")

    def test_detect_line_invalid_value(self):
        self.mock_sensor.readValue.return_value = "???"
        with self.assertRaises(ValueError):
            self.manager.detectLine()

    def test_detect_line_exception_from_sensor(self):
        self.mock_sensor.readValue.side_effect = TimeoutError("Capteur IR HS")
        with self.assertRaises(TimeoutError):
            self.manager.detectLine()


if __name__ == "__main__":
    unittest.main()