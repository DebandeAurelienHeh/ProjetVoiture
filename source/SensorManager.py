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
    def __init__(
        self,
        bus_i2C: busio.I2C = None,
        lineSensor=None,
        distSensorFront=None,
        distSensorLeft=None,
        distSensorRight=None,
        inaSensor=None,
        rgbSensor=None
    ):
        self.__i2c_bus = bus_i2C
        self.__lineSensor = lineSensor if lineSensor else LineSensor(20)
        self.__distSensorFront = distSensorFront if distSensorFront else DistanceSensor(6, 5, 'Front')
        self.__distSensorLeft = distSensorLeft if distSensorLeft else DistanceSensor(11, 9, 'Left')
        self.__distSensorRight = distSensorRight if distSensorRight else DistanceSensor(26, 19, 'Right')
        self.__isOnLine = False
        self.__inaSensor = inaSensor if inaSensor else INASensor(bus_i2C)
        self.__rgbSensor = rgbSensor if rgbSensor else RGBSensor(bus_i2C)

    def detectLine(self) -> bool:
        """
        Detect whether the car is currently over a line.
        Returns True if the IR sensor reads 0 (line detected),
        False if it reads 1 (no line),
        Raises ValueError for any unexpected value.
        """
        try:
            value = self.__lineSensor.readValue()

            if value == 0:
                self.__isOnLine = True
                return True
            elif value == 1:
                self.__isOnLine = False
                return False
            else:
                raise ValueError(f"Unexpected value returned by IR sensor: {value}")

        except Exception as e:
            print("Erreur lors de la détection de la ligne:", e)
        return False
  
    def getDistance(self) -> DistanceData:
        """
        Collects average distance measurements from three ultrasonic sensors
        using threading to speed up parallel reads.
        Returns a DistanceData object with front, left, and right distances.
        """
        results = [None, None, None]

        def wrapper(sensor, index):
            readings = []
            for _ in range(5):
                value = sensor.readValue()
                if value is not None:
                    readings.append(value)
                time.sleep(0.01)
            avg = round(sum(readings) / len(readings), 1) if readings else None
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

        return DistanceData(results[0], results[1], results[2])

    def getCurrent(self) -> float:
        """
        Retrieves the electrical current measured by the INA219 sensor.
        Returns the current in milliamps, or None if unavailable.
        """
        try:
            sensorData = self.__inaSensor.readValue()
            return sensorData.get('Current', None)
        except Exception as e:
            print("Error while reading current sensor:", e)
            return None

    def isRed(self, redMinimum: int = 150, G_R_DeltaMinimum: int = 30) -> bool:
        """
        Detects red color from RGB sensor data.
        Returns True if red value is high and significantly greater than green.
        """
        try:
            data = self.__rgbSensor.readValue()
            r = data.red
            g = data.green
            b = data.blue
            if r < redMinimum or (r - g) < G_R_DeltaMinimum:
                return False
            return True
        except Exception as e:
            print("Error while detecting red color:", e)
            return False

    def isGreen(self, greenMinimum: int = 150, G_R_DeltaMinimum: int = 50) -> bool:
        """
        Detects green color from RGB sensor data.
        Returns True if green value is high and significantly greater than red.
        """
        try:
            r, g, b = self.__rgbSensor.readValue()
            if g < greenMinimum or (g - r) < G_R_DeltaMinimum:
                return False
            return True
        except Exception as e:
            print("Error while detecting green color:", e)
            return False

if __name__ == "__main__":
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    sensor_manager = SensorManager(i2c_bus)

    while True:
        print("Current:", sensor_manager.getCurrent())
        time.sleep(1)
        print("RGB:", sensor_manager._SensorManager__rgbSensor.readValue())
        time.sleep(1)
        print("IS GREEN:", sensor_manager.isGreen())
        time.sleep(1)
        print("IS RED:", sensor_manager.isRed())
        time.sleep(1)
        print("Distance:", sensor_manager.getDistance())
        time.sleep(5)
