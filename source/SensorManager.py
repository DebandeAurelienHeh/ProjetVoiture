from LineSensor import LineSensor
from DistanceSensor import DistanceSensor
from RGBSensor import RGBSensor
from INASensor import INASensor
from data.DistanceData import DistanceData
import threading
import busio
import board
import time

class SensorManager:
    def __init__(self,bus_i2C:busio.I2C):
        self.__i2c_bus = bus_i2C
        self.__lineSensor = LineSensor(20)
        self.__distSensorFront = DistanceSensor(6,5,'Front')
        self.__distSensorLeft = DistanceSensor(11,9,'Left')
        self.__distSensorRight = DistanceSensor(26,19,'Right')
        self.__isOnLine = False
        self.__inaSensor = INASensor(bus_i2C)
        self.__rgbSensor = RGBSensor(bus_i2C)


    def detectLine(self) -> bool:
        """
        Detecte if the car is on the line.
        Return True if the car is on the line, False otherwise.
        """
        try:
            if not self.__isOnLine and self.__lineSensor.readValue():
                self.__isOnLine = True
                return True
            elif self.__isOnLine and not self.__lineSensor.readValue():
                self.__isOnLine = False
        except Exception as e:
            print("Erreur lors de la détection de la ligne:", e)
        return False
    
    def getDistance(self) -> DistanceData:
        """
        Return a tuple of the distances measured by the three distance sensors.
        The tuple contains:
        - distanceFront
        - distanceLeft
        - distanceRight
        Test 5 times the distance and return the average.
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

        data = DistanceData(results[0], results[1], results[2])
        return data

    def getCurrent(self) -> float:
        """
        Return the current measured by the INA219 sensor. If the sensor is not connected, return None.
        """
        try:
            sensorData = self.__inaSensor.readValue()
            return sensorData.get('Current', None)
        except Exception as e:
            print("Error while reading the sensor ", e)
            return None
    
    def isRed(self,redMinimum:int =150,G_R_DeltaMinimum:int =30) -> bool:
        """
        Detect if the color is red.
        The color is red if the red value is greater than redMinimum and the difference between 
        the green and red values is greater than G_R_DeltaMinimum.
        """
        try:
            data = self.__rgbSensor.readValue()
            r = data.red
            g = data.green
            b = data.blue
            if r < redMinimum:
                return False
            if (r - g) < G_R_DeltaMinimum:
                return False
            return True
        except Exception as e:
            print("Error while detecting a red :", e)
            return False

    def isGreen(self,greenMinimum:int = 150,G_R_DeltaMinimum:int = 50) -> bool:
        """
        Detect a presence of green.
        Green is considered detected if:
          - the value of G is greater than or equal to greenMinimum,
          - and if the difference (G - R) is greater than or equal to G_R_DeltaMinimum.
        """
        try:
            r, g, b = self.__rgbSensor.readValue()
            if g < greenMinimum:
                return False
            if (g - r) < G_R_DeltaMinimum:
                return False
            return True
        except Exception as e:
            print("Error while detecting the green: ", e)
            return False
        
i2c_bus = busio.I2C(board.SCL, board.SDA)
sensor_manager = SensorManager(i2c_bus)
while True:
   """ print("Current:", sensor_manager.getCurrent())
    time.sleep(1)
    print( "RGB:", sensor_manager.__rgbSensor.readValue())
    time.sleep(1)
    print("IS GREEN :", sensor_manager.isGreen())
    time.sleep(1)
    print("IS RED :", sensor_manager.isRed())
    time.sleep(1)<
    print("Distance:", sensor_manager.getDistance())
    time.sleep(5)"""