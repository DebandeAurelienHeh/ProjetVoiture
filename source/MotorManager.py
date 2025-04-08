from source.DCMotor import DCMotor
import adafruit_pca9685
import busio
import board
import time

class MotorManager():
    def __init__(self, i2c_bus:busio.I2C):
        self.__dcMotorsPropulsion = [DCMotor(5, 17, 18), DCMotor(4, 27, 22)]
        self.__i2c_bus = i2c_bus
        self.__pwmDriver = adafruit_pca9685.PCA9685(self.__i2c_bus, address=0x40)
        self.__pwmDriver.frequency = 60

    @property
    def dcMotorsPropulsion(self):
        return self.__dcMotorsPropulsion
    @property
    def i2c_bus(self):
        return self.__i2c_bus
    @property
    def pwmDriver(self):
        return self.__pwmDriver
    
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



