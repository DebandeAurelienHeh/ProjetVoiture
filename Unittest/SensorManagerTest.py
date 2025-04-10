import unittest
from unittest.mock import MagicMock, patch

from SensorManager import SensorManager

class TestSensorManager(unittest.TestCase):

    def setUp(self):
        self.sensor_manager = SensorManager()
        
        self.sensor_manager._SensorManager__lineSensor = MagicMock()
        self.sensor_manager._SensorManager__rgbSensor = MagicMock()
        self.sensor_manager._SensorManager__inaSensor = MagicMock()
        self.sensor_manager._SensorManager__distSensorFront = MagicMock()
        self.sensor_manager._SensorManager__distSensorLeft = MagicMock()
        self.sensor_manager._SensorManager__distSensorRight = MagicMock()

    def test_detectLine_true(self):
        self.sensor_manager._SensorManager__isOnLine = False
        self.sensor_manager._SensorManager__lineSensor.readValue.return_value = True
        self.assertTrue(self.sensor_manager.detectLine())

    def test_detectLine_false_after_true(self):
        self.sensor_manager._SensorManager__isOnLine = True
        self.sensor_manager._SensorManager__lineSensor.readValue.return_value = False
        self.assertFalse(self.sensor_manager.detectLine())
        self.assertFalse(self.sensor_manager._SensorManager__isOnLine)

    def test_getDistance_all_valid(self):
        for sensor in [
            self.sensor_manager._SensorManager__distSensorFront,
            self.sensor_manager._SensorManager__distSensorLeft,
            self.sensor_manager._SensorManager__distSensorRight
        ]:
            sensor.readValue.side_effect = [10, 12, 11, 13, 10]  # Moyenne = 11.2

        distances = self.sensor_manager.getDistance()
        self.assertEqual(distances, (11.2, 11.2, 11.2))

    def test_getDistance_with_invalids(self):
        # One sensor returns only None
        self.sensor_manager._SensorManager__distSensorFront.readValue.side_effect = [None] * 5
        self.sensor_manager._SensorManager__distSensorLeft.readValue.side_effect = [20, 21, 19, 20, 21]
        self.sensor_manager._SensorManager__distSensorRight.readValue.side_effect = [30, None, 30, 29, 31]

        distances = self.sensor_manager.getDistance()
        self.assertEqual(distances[0], None)
        self.assertEqual(distances[1], 20.2)
        self.assertEqual(distances[2], 30.0)

    def test_getCurrent_valid(self):
        self.sensor_manager._SensorManager__inaSensor.readValue.return_value = {'Current': 420}
        self.assertEqual(self.sensor_manager.getCurrent(), 420)

    def test_getCurrent_exception(self):
        self.sensor_manager._SensorManager__inaSensor.readValue.side_effect = Exception("INA error")
        self.assertIsNone(self.sensor_manager.getCurrent())

    def test_isRed_true(self):
        self.sensor_manager._SensorManager__rgbSensor.readValue.return_value = (180, 100, 50)
        self.assertTrue(self.sensor_manager.isRed())

    def test_isRed_false_low_r(self):
        self.sensor_manager._SensorManager__rgbSensor.readValue.return_value = (120, 110, 50)
        self.assertFalse(self.sensor_manager.isRed())

    def test_isRed_false_low_delta(self):
        self.sensor_manager._SensorManager__rgbSensor.readValue.return_value = (155, 140, 50)
        self.assertFalse(self.sensor_manager.isRed())

    def test_isGreen_true(self):
        self.sensor_manager._SensorManager__rgbSensor.readValue.return_value = (80, 170, 60)
        self.assertTrue(self.sensor_manager.isGreen())

    def test_isGreen_false_low_g(self):
        self.sensor_manager._SensorManager__rgbSensor.readValue.return_value = (60, 100, 60)
        self.assertFalse(self.sensor_manager.isGreen())

    def test_isGreen_false_low_delta(self):
        self.sensor_manager._SensorManager__rgbSensor.readValue.return_value = (140, 170, 60)
        self.assertFalse(self.sensor_manager.isGreen())

if __name__ == '__main__':
    unittest.main()
