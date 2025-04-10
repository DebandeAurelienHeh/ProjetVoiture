import time
from MotorManager import MotorManager
import logging
import busio
import board
from SensorManager import SensorManager
from logs_config import setup_logging
import threading

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
        self.__lock = threading.RLock()

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
        while True:
            with self.__lock:
                distances = self.sensorManager.getDistance()
                front_distance = distances.front
                left_distance = distances.left
                right_distance = distances.right

                self.motorManager.setSpeed(60)
                self.motorManager.setAngle(0)

                for _ in range(5):
                    time.sleep(0.1)

                if left_distance is not None and left_distance < 15:
                    self.logger.info(f"Left obstacle({left_distance} cm)")
                    self.turnRight()
                elif right_distance is not None and right_distance < 15:
                    self.logger.info(f"Right obstacle({right_distance} cm)")
                    self.turnLeft()
                elif front_distance is not None and front_distance < 30:
                    self.logger.info(f"Front obstacle ({front_distance} cm)")
                    if left_distance is not None and right_distance is not None:
                        if left_distance > right_distance:
                            self.turnLeft()
                        else:
                            self.turnRight()
                    elif left_distance is not None:
                        self.turnLeft()
                    elif right_distance is not None:
                        self.turnRight()

            for _ in range(5):
                time.sleep(0.1)

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
        self.__motorManager.setAngle(-50)
        time.sleep(0.5)
        self.__motorManager.setSpeed(75)
        self.__motorManager.setAngle(0)

    def turnRight(self):
        self.__motorManager.setSpeed(50)
        self.__motorManager.setAngle(50)
        time.sleep(0.5)
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

    def start_on_green(self):
        if self.__sensorManager.isGreen():
            self.logger.info("GREEN LIGHT! THE RACE IS ON!")

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