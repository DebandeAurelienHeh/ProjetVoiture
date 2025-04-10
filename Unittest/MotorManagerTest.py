import unittest
from unittest import mock
from unittest.mock import Mock, patch

import MotorManager as MotorManager
import adafruit_pca9685
import busio
import board
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'source')))

class TestMotorManager(unittest.TestCase):

    def setUp(self):
        servo_mock = Mock()
        servo_mock.centerAngle = 90
        servo_mock.rangeDegrees = 50
        servo_mock.minPulse = 1.0
        servo_mock.maxPulse = 2.0
        servo_mock.frequency = 60

        self.i2c_bus = busio.I2C(board.SCL, board.SDA)
        self.motorManager = MotorManager.MotorManager(self.i2c_bus)
        self.motorManager.__servoDirection = servo_mock

    @patch('DCMotor.DCMotor.stop')
    def testSetSpeed_when_0(self, mock):
        self.motorManager.setSpeed(0)
        self.assertTrue(mock.called)

    @patch('DCMotor.DCMotor.setDirection')
    def testSetSpeed_when_lower_than_0(self, mock):
        self.motorManager.setSpeed(-10)
        self.assertTrue(mock.called_with(False))

    @patch('DCMotor.DCMotor.setDirection')
    def testSetSpeed_when_higher_than_0(self, mock):
        self.motorManager.setSpeed(10)
        self.assertTrue(mock.called_with(True))

    @patch('MotorManager.MotorManager.convert_steering_to_duty', return_value=6990)
    @patch('MotorManager.MotorManager.pwmDriver')
    def testSetAngle(self, mock, mock2):
        self.motorManager.setAngle(0)
        self.assertTrue(mock.called_with(0))

    def testSetAngle_with_wrong_type(self):
        self.motorManager.setAngle("wrong_type")
        self.assertRaises(ValueError)

    def testConvertSteeringToDuty(self):
        result = self.motorManager.convert_steering_to_duty(100)
        expected = 6771
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()