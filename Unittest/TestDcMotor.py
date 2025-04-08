import unittest
from unittest.mock import patch
from DCMotor import DCMotor


class TestDCMotor(unittest.TestCase):

    @patch("DCMotor.GPIO")
    def test_set_direction_forward(self, mock_gpio):
        motor = DCMotor(1, 2, 3)
        motor.setDirection(True)

        mock_gpio.output.assert_any_call(2, mock_gpio.HIGH)
        mock_gpio.output.assert_any_call(3, mock_gpio.LOW)

    @patch("DCMotor.GPIO")
    def test_set_direction_backward(self, mock_gpio):
        motor = DCMotor(1, 2, 3)
        motor.setDirection(False)

        mock_gpio.output.assert_any_call(2, mock_gpio.LOW)
        mock_gpio.output.assert_any_call(3, mock_gpio.HIGH)

    @patch("DCMotor.GPIO")
    def test_stop_motor(self, mock_gpio):
        motor = DCMotor(1, 2, 3)
        motor.stop()

        mock_gpio.output.assert_any_call(2, mock_gpio.HIGH)
        mock_gpio.output.assert_any_call(3, mock_gpio.HIGH)


if __name__ == "__main__":
    unittest.main()
