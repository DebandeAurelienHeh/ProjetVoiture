import unittest
from unittest import mock
from unittest.mock import Mock, patch

import source.MotorManager as MotorManager

class TestMotorManager(unittest.TestCase):

    i2c_mock = Mock()

    def setUp(self):
        self.motorManager = MotorManager.MotorManager(self.i2c_mock)

    @patch('DCMotor.stop')
    def testSetSpeed_when_0(self, mock):
        self.motorManager.setSpeed(0)
        self.assertTrue(mock.called)

    @patch('DCMotor.direction')
    def testSetSpeed_when_lower_than_0(self, mock):
        self.motorManager.setSpeed(-10)
        self.assertTrue(mock.called_with(False))

    @patch('DCMotor.direction')
    def testSetSpeed_when_higher_than_0(self, mock):
        self.motorManager.setSpeed(10)
        self.assertTrue(mock.called_with(True))
