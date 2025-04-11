import RPi.GPIO as GPIO
import time
from Sensor import Sensor
import logging

class DistanceSensor(Sensor):
    def __init__(self, pinTrig: int, pinEcho: int, side: str):
        self.__pinTrig = pinTrig
        self.__pinEcho = pinEcho
        self.__side = side.capitalize()
        self.logger = logging.getLogger(__name__)

        GPIO.setup(self.__pinTrig, GPIO.OUT)
        GPIO.setup(self.__pinEcho, GPIO.IN)
    
    @property
    def side(self):
        return self.__side

    def readValue(self) -> float:
        try:
            GPIO.output(self.__pinTrig, True)
            time.sleep(0.00001)
            GPIO.output(self.__pinTrig, False)

            start_time = time.time()
            timeout = start_time + 0.05
            while GPIO.input(self.__pinEcho) == 0:
                start_time = time.time()
                if start_time > timeout:
                    self.logger.error("Start signal is too long.")
                    raise TimeoutError("Start signal is too long.")

            stop_time = time.time()
            timeout = stop_time + 0.05
            while GPIO.input(self.__pinEcho) == 1:
                stop_time = time.time()
                if stop_time > timeout:
                    self.logger.error("End signal is too long.")
                    raise TimeoutError("End signal is too long")

            duration = stop_time - start_time
            if duration <= 0:
                self.logger.error("Invalid duration.")
                raise ValueError("Invalid duration.")
            
            distance = round(duration * 17150, 2)

            if distance < 2 or distance > 400:
                self.logger.error(f"Distance out of range: {distance} cm")
                raise ValueError(f"Distance out of range: {distance} cm")
            
            return distance

        except Exception as e:
            print(f"[{self.__side}] Error : {e}")
            self.logger.error(f"[{self.__side}] Error : {e}")
            return None
        