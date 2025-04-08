from source.DCMotor import DCMotor
import adafruit_pca9685
import busio
import board
import time
import logging

class MotorManager():
    def __init__(self, i2c_bus:busio.I2C):
        self.__dcMotorsPropulsion = [DCMotor(5, 0, 1), DCMotor(4, 2, 3)]
        self.__i2c_bus = i2c_bus
        self.__pwmDriver = adafruit_pca9685.PCA9685(self.__i2c_bus)
        self.__pwmDriver.frequency = 60
        """
        Donne le nom de la classe aux logs
        """
        self.logger = logging.getLogger(__name__)

    def setSpeed(self, speed:float) -> None:
        
        """
        Définit la vitesse des moteurs DC.
        
        :param speed: Valeur comprise entre -100 et 100.
                      Un signe négatif indique la marche arrière, positif la marche avant, 0 arret.
        """
        if isinstance(speed, int) or isinstance(speed, float):
       
            front = (speed >= 0)
            speed_value = abs(speed)
            
            dc_duty = int((speed_value / 100.0) * 65535)
            
            for motor in self.__dcMotorsPropulsion:
                if speed_value == 0:
                    motor.stop()
                else:
                    motor.setDirection(front)
                    self.__pwmDriver.channels[motor.pinEnable].duty_cycle = dc_duty
        else:
            raise ValueError("Speed must be an integer or float.")
            self.logger.error("Speed must be an integer or float.")
            


i2c_bus = busio.I2C(board.SCL, board.SDA)
motor_manager = MotorManager(i2c_bus)
print(i2c_bus.scan())
motor_manager.setSpeed(0) 
time.sleep(3)
motor_manager.setSpeed(10) 
time.sleep(3)
motor_manager.setSpeed(50)
time.sleep(3)
motor_manager.setSpeed(70) 
time.sleep(3)
motor_manager.setSpeed(50)
time.sleep(3)
motor_manager.setSpeed(10)
time.sleep(3)
motor_manager.setSpeed(0)
motor_manager.setSpeed(-10)
time.sleep(3)
motor_manager.setSpeed(-50)
time.sleep(3)
motor_manager.setSpeed(-70)
time.sleep(3)
motor_manager.setSpeed(-50)
time.sleep(3)
motor_manager.setSpeed(-10)
time.sleep(3)
motor_manager.setSpeed(0)


