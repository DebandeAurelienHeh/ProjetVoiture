import time
from MotorManager import MotorManager
import logging
import busio
import board
from SensorManager import SensorManager
from logs_config import setup_logging

"""
Launch the logs functionality to log the informations in the file logs
"""
setup_logging()


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

    def selectMode(self) -> str:
        pass

    def detectObstacle(self):
        distances = self.sensorManager.getDistance()
        front_distance = distances[0]
        left_distance = distances[1]
        right_distance = distances[2]


        if left_distance is not None and left_distance < 15:
            self.logger.info(f"Obstacle trop proche à gauche ({left_distance} cm), virage à droite.")
            self.turnRight()

        elif right_distance is not None and right_distance < 15:
            self.logger.info(f"Obstacle trop proche à droite ({right_distance} cm), virage à gauche.")
            self.turnLeft()

        elif front_distance is not None and front_distance < 20:
            self.logger.info(f"Obstacle détecté devant à {front_distance} cm")
            if left_distance is not None and right_distance is not None:
                if left_distance > right_distance:
                    self.logger.info("Espace plus libre à gauche, virage à gauche.")
                    self.turnLeft()
                else:
                    self.logger.info("Espace plus libre à droite, virage à droite.")
                    self.turnRight()
            elif left_distance is not None:
                self.turnLeft()
            elif right_distance is not None:
                self.turnRight()

        else : 
            self.motorManager.setSpeed(75)
            self.motorManager.setAngle(0)
            time.sleep(1)


    def countLap(self) -> float:
        pass

    def startCar(self):
        self.__motorManager.setSpeed(25)
        time.sleep(1)
        self.__motorManager.setSpeed(50)
        time.sleep(1)
        self.__motorManager.setSpeed(75)

    def stopCar(self):
        self.__motorManager.setSpeed(0)
        self.__motorManager.setAngle(0)

    def reverseGear(self):
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
        for i in range(4):
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
        self.__motorManager.setSpeed(50)
        self.__motorManager.setAngle(-150)
        time.sleep(1)
        self.__motorManager.setSpeed(75)
        self.__motorManager.setAngle(0)

    def turnRight(self):
        self.__motorManager.setSpeed(50)
        self.__motorManager.setAngle(50)
        time.sleep(1)
        self.__motorManager.setSpeed(75)
        self.__motorManager.setAngle(0)

    def prepareMotors(self):
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

    def stayMid(self):
        """
        Adjust the car's speed and direction to stay centered between obstacles.

        This method uses three ultrasonic sensors (front, left, right) to determine the position 
        of the vehicle relative to its environment. Based on the distances, it calculates a new 
        steering angle and speed to keep the car centered while avoiding frontal collisions.

        Safety checks ensure the car stops if an obstacle is detected too close in front, 
        or if sensor data is missing or unreliable.

        Returns:
            tuple: A tuple (newSpeed, newAngle) indicating the speed (0–100) and angle (-100 to 100)
                applied to the car's motors.
        """
        frontDist, leftDist, rightDist = self.__sensorManager.getDistance()

        # Constants
        min_front = 20
        max_front = 100
        Kp = 10

        # Stop if an obstacle is detected in front or the front sensor fails
        if frontDist is None or frontDist < min_front:
            self.__motorManager.setSpeed(0)
            self.__motorManager.setAngle(0)
            return (0, 0)

        # Handle cases where side sensors fail
        if leftDist is None and rightDist is None:
            self.__motorManager.setSpeed(0)
            self.__motorManager.setAngle(0)
            return (0, 0)
        elif leftDist is None:
            error = 1  # Slightly steer left to stay away from the unknown right side
        elif rightDist is None:
            error = -1  # Slightly steer right to stay away from the unknown left side
        else:
            error = rightDist - leftDist

        # Compute steering angle
        newAngle = max(-100, min(100, Kp * error))

        # Compute speed based on frontal distance
        try:
            rawSpeed = (frontDist - min_front) / (max_front - min_front) * 100
        except ZeroDivisionError:
            rawSpeed = 0

        newSpeed = max(0, min(100, rawSpeed))

        # Reduce speed in curves
        correctionFactor = 1 - (abs(newAngle) / 100) * 0.5
        newSpeed *= correctionFactor

        # Apply motor commands
        self.__motorManager.setAngle(newAngle)
        self.__motorManager.setSpeed(newSpeed)

        return (newSpeed, newAngle)

def main():
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    lambo = LamboCar(i2c_bus)
    lambo.prepareMotors()
    time.sleep(2)
    lambo.reverseGear()
    print("Reversing gear done")
    lambo.eightTurn(1)
    print("Eight turn done")
    lambo.uTurn()
    print("U turn done")

if __name__ == "__main__":
    main()