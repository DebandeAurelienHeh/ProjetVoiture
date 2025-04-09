from DistanceSensor import DistanceSensor
import threading 
import busio
import board
import time

class SensorManager:
    def __init__(self, bus_i2C:busio.I2C):
        self.__i2c_bus = bus_i2C
        self.__distSensorFront = DistanceSensor(6,5,'Front')
        self.__distSensorLeft = DistanceSensor(11,9,'Left')
        self.__distSensorRight = DistanceSensor(26,19,'Right')
    
    def getDistance(self) -> tuple:
        """
        Get the distance from the three sensors (front, left, right) using threading.
        Each sensor's reading is averaged over 5 attempts to ensure accuracy.
        The results are returned as a tuple in the order of (front, left, right).
        """
        results = [None, None, None]

        def wrapper(sensor, index):
            readings = []
            for _ in range(5):
                value = sensor.readValue()
                if value is not None:
                    readings.append(value)
                time.sleep(0.01) 
            if readings:
                avg = round(sum(readings) / len(readings),1)
            else:
                avg = None 
            results[index] = avg

        threads = [
            threading.Thread(target=wrapper, args=(self.__distSensorFront, 0)),
            threading.Thread(target=wrapper, args=(self.__distSensorLeft, 1)),
            threading.Thread(target=wrapper, args=(self.__distSensorRight, 2))
        ]
        
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return tuple(results)

