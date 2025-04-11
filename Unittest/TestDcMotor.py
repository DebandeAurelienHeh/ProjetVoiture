import unittest
from unittest.mock import patch
from DCMotor import DCMotor
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'source')))


class TestDCMotor(unittest.TestCase):

    def setUp(self):
        self.motor = DCMotor(5, 17, 18)

    @patch("DCMotor.GPIO")
    def test_set_direction_forward(self, mock_gpio):
        """
        This test checks if the motor is set to move forward by setting the direction pins correctly.
        It uses the mock GPIO library to simulate the GPIO behavior and verifies the output.
        """
        self.motor.setDirection(True)

        mock_gpio.output.assert_any_call(17, mock_gpio.LOW)
        mock_gpio.output.assert_any_call(18, mock_gpio.HIGH)

    @patch("DCMotor.GPIO")
    def test_set_direction_backward(self, mock_gpio):
        """
        This test checks if the motor is set to move backward by setting the direction pins correctly.
        It uses the mock GPIO library to simulate the GPIO behavior and verifies the output.
        """
        self.motor.setDirection(False)

        mock_gpio.output.assert_any_call(17, mock_gpio.HIGH)
        mock_gpio.output.assert_any_call(18, mock_gpio.LOW)

    @patch("DCMotor.GPIO")
    def test_stop_motor(self, mock_gpio):
        """
        This test checks if the motor is stopped by setting both direction pins to HIGH.
        It uses the mock GPIO library to simulate the GPIO behavior and verifies the output.
        """
        self.motor.stop()

        mock_gpio.output.assert_any_call(17, mock_gpio.HIGH)
        mock_gpio.output.assert_any_call(18, mock_gpio.HIGH)


if __name__ == "__main__":
    unittest.main()
