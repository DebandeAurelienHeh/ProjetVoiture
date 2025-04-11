import unittest
from unittest.mock import Mock, patch

"""

This is a mockup of a RGB sensor reading function and two functions to check if the color is green or red.
The functions are then tested using unittest and unittest.mock.

"""

class RGBSensor:
    def read_rgb(self):
        pass

    def isGreen(self, green_minimum, G_R_DeltaMin):
        rgb = self.read_rgb()
        if green_minimum < rgb[1] and rgb[1] - rgb[0] >= G_R_DeltaMin:
            return True
        return False

    def isRed(self, red_minimum, R_G_DeltaMin):
        rgb = self.read_rgb()
        if red_minimum < rgb[0] and rgb[0] - rgb[1] >= R_G_DeltaMin:
            return True
        return False

class TestRGBSensor(unittest.TestCase):
    def setUp(self):
        self.sensor = RGBSensor()
        self.sensor.read_rgb = Mock()

    def test_read_rgb(self):
        self.sensor.read_rgb.return_value = (255, 0, 0)
        result = self.sensor.read_rgb()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(0 <= x <= 255 for x in result))

    def test_isGreen(self):
        self.sensor.read_rgb.return_value = (155, 255, 0)
        result = self.sensor.isGreen(130, 50)
        self.assertTrue(result)

        self.sensor.read_rgb.return_value = (255, 0, 0)
        result = self.sensor.isGreen(130, 50)
        self.assertFalse(result)
        
    def test_isRed(self):
        self.sensor.read_rgb.return_value = (255, 0, 0)
        result = self.sensor.isRed(130, 50)
        self.assertTrue(result)

        self.sensor.read_rgb.return_value = (0, 255, 0)
        result = self.sensor.isRed(130, 50)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()