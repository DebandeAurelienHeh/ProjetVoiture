import time
import logging
import threading
import busio
import board
from MotorManager import MotorManager
from SensorManager import SensorManager
from logs_config import setup_logging

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
        self.__tour = 0
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

    def LineCount(self):
        try:
            on_line = self.sensorManager.detectLine()
            if on_line and not self.__last_line_state:
                self.__tour += 1
                self.logger.info(f"Lap counted! Total laps: {self.__tour}")
            self.__last_line_state = on_line
        except Exception as e:
            self.logger.error(f"Error in LineCount: {e}")

    def detectObstacle(self):
        while True:
            with self.__lock:
                distances = self.sensorManager.getDistance()
                front_distance = distances.front
                left_distance = distances.left
                right_distance = distances.right

                self.motorManager.setSpeed(50)
                self.motorManager.setAngle(0)
                time.sleep(0.1)

                if front_distance is not None and front_distance < 30:
                    self.logger.info(f"Front obstacle detected ({front_distance} cm)")
                    time.sleep(1)

                    left = left_distance if left_distance is not None else 0
                    right = right_distance if right_distance is not None else 0
                    self.logger.info(f"Left: {left} cm, Right: {right} cm")

                    self.motorManager.setSpeed(-40)
                    time.sleep(0.7)
                    self.motorManager.setSpeed(0)

                    if left > right:
                        self.logger.info("Turning left (more space)")
                        self.turnLeft()
                    else:
                        self.logger.info("Turning right (more space)")
                        self.turnRight()

                elif left_distance is not None and left_distance < 15:
                    self.logger.info(f"Left obstacle ({left_distance} cm)")
                    self.turnRight()
                elif right_distance is not None and right_distance < 15:
                    self.logger.info(f"Right obstacle ({right_distance} cm)")
                    self.turnLeft()

            time.sleep(0.1)

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
        self.__motorManager.setSpeed(30)
        self.__motorManager.setAngle(-60)
        time.sleep(0.5)

    def turnRight(self):
        self.__motorManager.setSpeed(30)
        self.__motorManager.setAngle(60)
        time.sleep(0.5)

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

    def start_on_green(self):
        if self.__sensorManager.isGreen():
            self.logger.info("GREEN LIGHT! THE RACE IS ON!")

    def stayMid(self):
        frontDist, leftDist, rightDist = self.__sensorManager.getDistance()

        min_front = 20
        max_front = 100
        Kp = 10

        if frontDist is None or frontDist < min_front:
            self.__motorManager.setSpeed(-30)
            time.sleep(1)                       #ça a été rajouté pour éviter que la voiture ne recule trop
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
            rawSpeed = 10
            #Moteur n'avancerait pas avec la vitesse trop basse

        newSpeed = max(10, min(100, rawSpeed))
        correctionFactor = 1 - (abs(newAngle) / 100) * 0.5
        newSpeed *= correctionFactor

        self.__motorManager.setAngle(newAngle)
        self.__motorManager.setSpeed(newSpeed)

        return (newSpeed, newAngle)


def main():
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    lambo = LamboCar(i2c_bus)

    lambo.prepareMotors()
    time.sleep(2)

    obstacle_thread = threading.Thread(target=lambo.detectObstacle, daemon=True)
    obstacle_thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stop the car.")
        lambo.stopCar()


if __name__ == "__main__":
    main()