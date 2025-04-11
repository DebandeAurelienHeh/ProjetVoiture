import time
import logging
import threading
import busio
import board
from MotorManager import MotorManager
from SensorManager import SensorManager
from logs_config import setup_logging

setup_logging()

"""
LamboCar class for controlling a car with motors and sensors.
This class provides methods to control the car's movement, manage sensors, and perform various maneuvers.
It also includes methods for lap counting and obstacle avoidance.
"""
class LamboCar:
    def __init__(self, i2c_bus: busio.I2C):
        self.__carName = "LamboCar"
        self.__sensorManager = SensorManager(i2c_bus)
        self.__motorManager = MotorManager(i2c_bus)
        self.__totalLaps = 0
        self.__lastLapDuration = 0
        self.__currentState = ""
        self.__constConfig = {}
        self.__mode = None
        self.__tour = -1
        self.__last_line_state = False
        self.__lock = threading.RLock()
        self.logger = logging.getLogger(__name__)

    @property
    def motorManager(self):
        return self.__motorManager

    @property
    def sensorManager(self):
        return self.__sensorManager

    @property
    def carName(self):
        return self.__carName

    @property
    def mode(self):
        return self.__mode

    @property
    def totalLaps(self):
        return self.__totalLaps

    @property
    def lastLapDuration(self):
        return self.__lastLapDuration

    @property
    def tour(self):
        return self.__tour

    @property
    def countLap(self):
        return self.__tour

    @tour.setter
    def tour(self, tour):
        self.__tour = tour

    def LineCount(self):
        """
        Counts laps based on line detection.
        Increments the lap count when a line is detected.
        """
        try:
            on_line = self.sensorManager.detectLine()
            if on_line and not self.__last_line_state:
                self.__tour += 1
                self.logger.info(f"Lap counted! Total laps: {self.__tour}")
            self.__last_line_state = on_line
        except Exception as e:
            self.logger.error(f"Error in LineCount: {e}")

    def startCar(self):
        """
        Starts the car by setting the speed and angle of the motors.
        Gradually increases the speed to avoid sudden acceleration.
        """
        self.__motorManager.setSpeed(25)
        time.sleep(1)
        self.__motorManager.setSpeed(50)
        time.sleep(1)
        self.__motorManager.setSpeed(75)

    def stopCar(self):
        """
        Stops the car by setting the speed and angle of the motors to zero.
        """
        self.__motorManager.setSpeed(0)
        self.__motorManager.setAngle(0)

    def reverseGear(self):
        """
        Reverses the car by setting the speed to negative values.
        Gradually decreases the speed to avoid sudden deceleration.
        """
        self.logger.info("The car is going forward")
        self.__motorManager.setSpeed(25)
        time.sleep(2)
        self.__motorManager.setSpeed(50)
        time.sleep(2)
        self.__motorManager.setSpeed(75)
        time.sleep(1)
        self.__motorManager.setSpeed(0)
        self.logger.info("The car is stopping")
        time.sleep(2)
        self.logger.info("The car is going backward")
        self.__motorManager.setSpeed(-25)
        time.sleep(2)
        self.__motorManager.setSpeed(-50)
        time.sleep(2)
        self.__motorManager.setSpeed(-75)
        time.sleep(1)
        self.__motorManager.setSpeed(0)
        self.logger.info("The car is stopping")

    def uTurn(self):
        """
        Performs a U-turn by setting the speed and angle of the motors.
        The car turns in place for a specified duration before stopping.
        """
        for _ in range(4):
            self.__motorManager.setAngle(-100)
            self.__motorManager.setSpeed(-25)
            time.sleep(1)
            self.__motorManager.setAngle(20)
            self.__motorManager.setSpeed(10)
            time.sleep(1)
        self.__motorManager.setAngle(0)
        self.__motorManager.setSpeed(40)
        time.sleep(1)
        self.__motorManager.setSpeed(0)

    def circle(self, direction: str):
        """
        Performs a circular motion by setting the speed and angle of the motors.
        The direction can be either 'left' or 'right'.
        """
        self.__motorManager.setSpeed(50)
        if direction.lower() == "left":
            self.__motorManager.setAngle(-100)
        elif direction.lower() == "right":
            self.__motorManager.setAngle(100)
        else:
            self.logger.error("Circle: Invalid direction, it must be 'left' or 'right'")
            raise ValueError("Direction must be 'left' or 'right'")
        time.sleep(10)
        self.__motorManager.setAngle(0)
        self.__motorManager.setSpeed(0)

    def eightTurn(self, duration: int):
        """
        Performs an eight-turn maneuver by alternating between left and right turns.
        The duration specifies how many times the turn is performed.
        """
        self.__motorManager.setSpeed(40)
        for _ in range(duration):
            self.__motorManager.setAngle(-100)
            self.logger.info("eightTurn: Turning left")
            time.sleep(8)
            self.__motorManager.setAngle(90)
            self.logger.info("eightTurn: Turning right")
            time.sleep(6)
        self.__motorManager.setAngle(0)
        self.__motorManager.setSpeed(0)

    def turnLeft(self):
        self.__motorManager.setSpeed(30)
        self.__motorManager.setAngle(-60)
        time.sleep(0.5)

    def turnRight(self):
        self.__motorManager.setSpeed(30)
        self.__motorManager.setAngle(60)
        time.sleep(0.5)

    def prepareMotors(self):
        """
        Tests the motors for operation by setting their speed and angle.
        """
        print("Preparing DC motors...")
        self.__motorManager.setSpeed(0)
        time.sleep(0.5)
        self.__motorManager.setSpeed(25)
        time.sleep(0.25)
        self.__motorManager.setSpeed(0)
        time.sleep(0.25)
        self.__motorManager.setSpeed(-25)
        time.sleep(0.25)
        self.__motorManager.setSpeed(0)
        time.sleep(0.5)
        print("Motors DC are prepared")
        self.logger.info("Motors DC : Ok!")

        print("Preparing Servo motors...")
        self.__motorManager.setAngle(0)
        time.sleep(0.5)
        self.__motorManager.setAngle(50)
        time.sleep(1)
        self.__motorManager.setAngle(0)
        time.sleep(1)
        self.__motorManager.setAngle(-50)
        time.sleep(1)
        self.__motorManager.setAngle(0)
        time.sleep(1)
        print("Servo motors are prepared")
        self.logger.info("Servo motors : Ok!")

    def prepareSensors(self):
        """
        Tests the sensors for operation by reading their values and checking their responses.
        """
        print("Preparing sensors...")
        all_ready = True

        data_rgb = self.__sensorManager.rgbSensor.readValue()
        if data_rgb is not None:
            red, green, blue = data_rgb.red, data_rgb.green, data_rgb.blue
            print(f"RGB Sensor: Red: {red}, Green: {green}, Blue: {blue}")
            self.logger.info("RGB Sensor is ready")
            print("RGB Sensor is ready!")
        else:
            print("RGB Sensor does not respond!")
            self.logger.error("RGB Sensor does not respond!")
            all_ready = False

        data_ina = self.__sensorManager.getCurrent()
        if data_ina is not None:
            print(f"Current in milliamps: {data_ina}")
            self.logger.info(f"INA219 sensor is ready. Current in milliamps: {data_ina}")
            print("INA219 sensor is ready!")
        else:
            print("INA219 sensor does not respond!")
            self.logger.error("INA219 sensor does not respond!")
            all_ready = False

        data_dist = self.__sensorManager.getDistance()
        if data_dist is not None:
            front, left, right = data_dist.front, data_dist.left, data_dist.right
            print(f"Distance: Front: {front}, Left: {left}, Right: {right}")
            self.logger.info("Distance sensors are ready")
            print("Distance sensors are ready!")
        else:
            print("Distance sensors do not respond!")
            self.logger.error("Distance sensors do not respond!")
            all_ready = False

        data_line = self.__sensorManager.detectLine()
        if data_line is not None:
            print(f"Line sensor does not detect black line: {data_line}")
            self.logger.info("Line sensor is ready")
            print("Line sensor is ready!")
        else:
            print("Line sensor does not respond!")
            self.logger.error("Line sensor does not respond!")
            all_ready = False
        if all_ready:
            print("All sensors are ready!")
            self.logger.info("All sensors are ready!")
        else:
            print("Some sensors are not responding!")
            self.logger.error("Some sensors are not responding!")
        return all_ready

    def start_on_green(self, tours):
        """
        Starts the car when the green light is detected.
        Continuously checks the sensor for the green light and starts the car when detected."""
        while True:
            if self.__sensorManager.isGreen():
                self.logger.info("GREEN LIGHT! THE RACE IS ON!")
                self.start(tours)
            else:
                self.logger.info("NOT GREEN YET!")
                time.sleep(0.5)

    def stayMid(self):
        """
        Keeps the car in the middle of the track by adjusting the speed and angle based on sensor readings.
        """
        distance = self.__sensorManager.getDistance()
        frontDist = distance.front
        leftDist = distance.left
        rightDist = distance.right

        min_front = 20
        max_front = 100
        Kp = 10

        if frontDist is None or frontDist < min_front:
            self.__motorManager.setSpeed(-30)
            time.sleep(1)  
            self.__motorManager.setAngle(0)
            return (-30, 0)

        if leftDist is None and rightDist is None:
            self.__motorManager.setSpeed(0)
            self.__motorManager.setAngle(0)
            return (0, 0)
        
        elif leftDist is None:
            error = 1
        elif rightDist is None:
            error = -1
        else:
            error = rightDist - leftDist

        newAngle = max(-100, min(100, Kp * error))

        try:
            rawSpeed = (frontDist - min_front) / (max_front - min_front) * 100
        except ZeroDivisionError:
            rawSpeed = 40

        newSpeed = max(40, min(41, rawSpeed))
        correctionFactor = 1 - (abs(newAngle) / 100) * 0.5
        newSpeed *= correctionFactor

        self.__motorManager.setAngle(newAngle)
        self.__motorManager.setSpeed(newSpeed)

        return (newSpeed, newAngle)

    def test(self):
        """
        Test function to prepare the car for operation.
        """
        self.prepareMotors()
        time.sleep(1)
        self.prepareSensors()
        time.sleep(1)
        self.start()

    def start(self, max_tours):
        """
        Starts the car and counts laps based on line detection.
        """
        line_detected = False
        try:
            while self.tour < max_tours:
                self.stayMid()

                if self.sensorManager.detectLine() and not line_detected:
                    self.tour+=1
                    self.logger.info(self.tour)
                    line_detected = True
                    time.sleep(0.5)
                elif self.sensorManager.detectLine():
                    line_detected = False
                time.sleep(0.5)
            self.stopCar()
        except KeyboardInterrupt:
            print("Stop the car.")
            self.stopCar()

    def zigzagAvoidance(self):
        """
        Zigzag avoidance maneuver to navigate around obstacles.
        The car turns right and left alternately when an obstacle is detected within a certain distance.
        """
        try :
            self.__motorManager.setSpeed(45)
            self.__motorManager.setAngle(0)

            while True:
                distance = self.__sensorManager.getDistance().front

                if distance is not None and distance < 50:
                    self.logger.info(f"Obstacle detected at {distance} cm → initiating zigzag")

                    self.__motorManager.setAngle(80)
                    time.sleep(1.2)

                    self.__motorManager.setAngle(-90)
                    time.sleep(1.5)

                    self.__motorManager.setAngle(0)

                else:
                    self.__motorManager.setSpeed(30)
                    self.__motorManager.setAngle(0)

                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Stop the car.")
            self.stopCar()

def main():
    """
    Main function to initialize the LamboCar and start the car.
    """
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    lambo = LamboCar(i2c_bus)

    try:
        while True:
            lambo.stayMid()
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Stop the car.")
        lambo.stopCar()

if __name__ == "__main__":
    main()
