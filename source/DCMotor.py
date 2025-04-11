import RPi.GPIO as GPIO
"""
DCMotor class for controlling a DC motor using GPIO pins on a Raspberry Pi.
This class allows you to set the direction of the motor and stop it.
"""
class DCMotor:
    def __init__(self, enable, input1, input2):
        self.__pinEnable = enable
        self.__pinInput1 = input1
        self.__pinInput2 = input2

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pinEnable, GPIO.OUT)
        GPIO.setup(self.__pinInput1, GPIO.OUT)
        GPIO.setup(self.__pinInput2, GPIO.OUT)

    @property
    def pinEnable(self):
        return self.__pinEnable

    @property
    def pinInput1(self):
        return self.__pinInput1

    @property
    def pinInput2(self):
        return self.__pinInput2

    def setDirection(self, direction):
        """Set the direction of the motor.
        Args:
            direction (bool): True for one direction, False for the opposite.
        """
        if direction:
            GPIO.output(self.__pinInput1, GPIO.LOW)
            GPIO.output(self.__pinInput2, GPIO.HIGH)
        elif not direction:
            GPIO.output(self.__pinInput1, GPIO.HIGH)
            GPIO.output(self.__pinInput2, GPIO.LOW)

    def stop(self):
        """
        Stop the motor.
        """
        GPIO.output(self.__pinInput1, GPIO.HIGH)
        GPIO.output(self.__pinInput2, GPIO.HIGH)

