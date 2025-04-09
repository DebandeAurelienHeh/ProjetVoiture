import time
from MotorManager import MotorManager
import logging
import busio
import board
#from logs_config import setup_logging
"""
Launch the logs functionality to log the informations in the file logs
"""
#setup_logging()

class LamboCar:
    def __init__(self, i2c_bus: busio.I2C):
        self.__carName = "LamboCar"
        self.__sensorManager = None
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

    def detectObstacle(self) -> None:
        pass

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

    def reverseGear(self):
        self.__motorManager.setSpeed(25)
        time.sleep(2)
        self.__motorManager.setSpeed(50)
        time.sleep(2)
        self.__motorManager.setSpeed(75)
        time.sleep(1)
        self.__motorManager.setSpeed(0)
        time.sleep(2)
        self.__motorManager.setSpeed(-25)
        time.sleep(2)
        self.__motorManager.setSpeed(-50)
        time.sleep(2)
        self.__motorManager.setSpeed(-75)
        time.sleep(1)
        self.__motorManager.setSpeed(0)

    def uTurn(self):
        self.__motorManager.setSpeed(50) 
        self.__motorManager.setAngle(-100)   
        time.sleep(5)
        self.__motorManager.setSpeed(75) 

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
        self.__motorManager.setSpeed(50)  
        for _ in range(duration):
            self.__motorManager.setAngle(-90)
            self.logger.info("eightTurn: Turning left")
            time.sleep(3)
            self.__motorManager.setAngle(90)
            self.logger.info("eightTurn: Turning right")
            time.sleep(3)
        
        self.__motorManager.setAngle(0)
        self.__motorManager.setSpeed(0)

    def turnLeft(self):
        self.__motorManager.setSpeed(50)     
        self.__motorManager.setAngle(-100)    
        time.sleep(1) 
        self.__motorManager.setSpeed(75)                     
        self.__motorManager.setAngle(0)       

    def turnRight(self):
        self.__motorManager.setSpeed(50)
        self.__motorManager.setAngle(100)
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


i2c_bus = busio.I2C(board.SCL, board.SDA)
lambo = LamboCar(i2c_bus)

lambo.prepareMotors()
time.sleep(2)
lambo.reverseGear()
print("Reversing gear done")

