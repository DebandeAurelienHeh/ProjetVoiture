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
        Renvoie un tuple des distances (Front, Left, Right) en cm.
        Pour chaque capteur, 5 mesures sont effectuées et la moyenne des lectures valides est calculée.
        En cas d'erreur, la mesure sera ignorée.
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

i2c_bus = busio.I2C(board.SCL, board.SDA)
sensor_manager = SensorManager(i2c_bus)
while True:
    print(sensor_manager.getDistance())