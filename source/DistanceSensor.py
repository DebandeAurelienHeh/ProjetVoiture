import RPi.GPIO as GPIO
import time
from Sensor import Sensor


class DistanceSensor(Sensor):
    def __init__(self, pinTrig: int, pinEcho: int, side: str):
        self.__pinTrig = pinTrig
        self.__pinEcho = pinEcho
        self.__side = side.capitalize()

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
                    raise TimeoutError("Début du signal trop long.")

            stop_time = time.time()
            timeout = stop_time + 0.05
            while GPIO.input(self.__pinEcho) == 1:
                stop_time = time.time()
                if stop_time > timeout:
                    raise TimeoutError("Fin du signal trop long.")

            duration = stop_time - start_time
            if duration <= 0:
                raise ValueError("Durée invalide.")
            
            distance = round(duration * 17150, 2)

            if distance < 2 or distance > 400:
                raise ValueError(f"Hors limites : {distance} cm")
            
            return distance

        except Exception as e:
            print(f"[{self.__side}] Erreur : {e}")
            return None

    