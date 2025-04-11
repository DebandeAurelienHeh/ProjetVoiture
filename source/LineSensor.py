from Sensor import Sensor
import RPi.GPIO as GPIO
import time

class LineSensor(Sensor):
    def __init__(self,pinGPIO:int):
        self.__pinGPIO = pinGPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pinGPIO,GPIO.IN)
    
    @property
    def pinGPIO(self):
        return self.__pinGPIO

    def readValue(self, timeout: float = 1.0) -> bool:
        """ 
        Returns True if the line is detected (value 0),
        returns False otherwise (value 1),
        and raises a TimeoutError if no stable reading is achieved within the allotted timeout.
        """
        start_time = time.time()
        
        while True:
            result = GPIO.input(self.__pinGPIO)
            if result == 0:
                return True
            elif result == 1:
                return False
            
            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout waiting for a valid GPIO value")
            
            time.sleep(0.001)

        
    