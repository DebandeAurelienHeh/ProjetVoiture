import time
from MotorManager import MotorManager

class LamboCar:
    def __init__(self):
        self.__carName = "LamboCar"
        self.__sensorManager = None            
        self.__motoManager = None             
        self.__totalLaps = 0
        self.__lastLapDuration = 0
        self.__currentState = ""
        self.__constConfig = {}
        self.__mode = None           

    @property
    def motoManager(self):
        return self.__motoManager

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
        self.__motoManager.setSpeed(25)
        time.sleep(1)
        self.__motoManager.setSpeed(50)
        time.sleep(1)
        self.__motoManager.setSpeed(75)

    def stopCar(self):
        self.__motoManager.setSpeed(0)

    def reverseGear(self):
        self.__motoManager.setSpeed(25)
        time.sleep(2)
        self.__motoManager.setSpeed(50)
        time.sleep(2)
        self.__motoManager.setSpeed(75)
        time.sleep(1)
        self.__motoManager.setSpeed(0)
        time.sleep(2)
        self.__motoManager.setSpeed(-25)
        time.sleep(2)
        self.__motoManager.setSpeed(-50)
        time.sleep(2)
        self.__motoManager.setSpeed(-75)
        time.sleep(1)
        self.__motoManager.setSpeed(0)

    def uTurn(self):
        self.__motoManager.setSpeed(50) 
        self.__motoManager.setAngle(-100)   
        time.sleep(5)
        self.__motoManager.setSpeed(75) 

    def circle(self, direction: str):
        self.__motoManager.setSpeed(50)

        if direction.lower() == "left":
            self.__motoManager.setAngle(-100)
        elif direction.lower() == "right":
            self.__motoManager.setAngle(100)
        else:
            raise ValueError("Direction doit être 'left' ou 'right'")

        time.sleep(10)
        self.__motoManager.setAngle(0)
        self.__motoManager.setSpeed(0)

    def eightTurn(self, duration: int):
        self.__motoManager.setSpeed(50)  
        for _ in range(duration):
            self.__motoManager.setAngle(-100)
            time.sleep(5)
            self.__motoManager.setAngle(100)
            time.sleep(5)
        
        self.__motoManager.setAngle(0)
        self.__motoManager.setSpeed(0)

    def turnLeft(self):
        self.__motoManager.setSpeed(50)     
        self.__motoManager.setAngle(-100)    
        time.sleep(1) 
        self.__motoManager.setSpeed(75)                     
        self.__motoManager.setAngle(0)       

    def turnRight(self):
        self.__motoManager.setSpeed(50)
        self.__motoManager.setAngle(100)
        time.sleep(1)
        self.__motoManager.setSpeed(75)
        self.__motoManager.setAngle(0)
