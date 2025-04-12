from DCMotor import DCMotor
from ServoMotor import ServoMotor
import adafruit_pca9685
import busio
import board
import time

class MotorManager():
    def __init__(self, i2c_bus:busio.I2C):
        self.__dcMotorsPropulsion = [DCMotor(5, 17, 18), DCMotor(4, 27, 22)]
        self.__servoDirection = ServoMotor(0, 50)
        self.__i2c_bus = i2c_bus
        self.__pwmDriver = adafruit_pca9685.PCA9685(self.__i2c_bus, address=0x40)
        self.__pwmDriver.frequency = 50

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
        try:
            """
            Sets the speed of the DC motors.

            :param speed: Value between -100 and 100.
            A negative value indicates reverse,
            a positive value indicates forward,
            and 0 stops the motor.
            """
            if isinstance(speed, int) or isinstance(speed, float):

                front = (speed >= 0)
                speed_value = abs(speed)

                dc_duty = int((speed_value / 100.0) * 65535)

                for motor in self.__dcMotorsPropulsion:
                    if speed_value == 0:
                        motor.stop()
                        print("Speed is 0, motors stopped.")
                    else:
                        motor.setDirection(front)
                        self.__pwmDriver.channels[motor.pinEnable].duty_cycle =((2**16)-1)-dc_duty
                        if front:
                            print(f"Motors are moving forward at {speed_value}%.")
                        else:
                            print(f"Motors are moving backward at {speed_value}%.")

            else:
                raise ValueError("Speed must be an integer or float.")
        except ValueError as e:
            print(e)
        
    def setAngle(self, steering:float) -> None:
        try:
            """
            Sets the angle for the steering servo.

            :param steering: Steering percentage from -100 (full left) to 100 (full right), 0 for straight ahead.
            """
            if isinstance(steering, int) or isinstance(steering, float):
                servo_duty = self.convert_steering_to_duty(steering)
                self.__pwmDriver.channels[self.__servoDirection.boardChannel].duty_cycle = ((2**16)-1)-servo_duty
            else:
                raise ValueError("Steering must be an integer or float.")
        except ValueError as e:
            print(e)
        
    def convert_steering_to_duty(self, steering: float) -> int:
        """
        Converts a steering percentage (-100 to 100) into a duty_cycle value (0 to 65535)
        for a servo with a limited mechanical range around the center.

        Parameters:
        - steering: Steering percentage (-100 to 100)
        - center_angle: The center angle of the servo (in degrees), typically 90°.
        - range_deg: Maximum deviation from the center, e.g., 45°.
                    This means -100% corresponds to center_angle - range_deg (90-45 = 45°)
                    and 100% to center_angle + range_deg (90+45 = 135°).
        - freq: PWM signal frequency (e.g., 60 Hz)
        - min_pulse_ms: Minimum pulse width in ms (for 0° in the full mapping, e.g., 1.0 ms)
        - max_pulse_ms: Maximum pulse width in ms (for 180° in the full mapping, e.g., 2.0 ms)

        The function first calculates the signal period, determines the full duty cycle range
        for the servo, then extracts the value corresponding to the effective angle.

        :return: 16-bit duty_cycle value (0 to 65535)
        """
        center_angle = self.__servoDirection.centerAngle
        range_deg = self.__servoDirection.rangeDegrees
        min_pulse_ms = self.__servoDirection.minPulse
        max_pulse_ms = self.__servoDirection.maxPulse
        freq = self.__servoDirection.frequency

        periode_ms = 1000.0 / freq  # ex: 1000/60 ≈ 16.67 ms
        
        t_min_duty = min_pulse_ms / periode_ms   # ex: ≈ 1.0/16.67 ≈ 0.06
        t_max_duty = max_pulse_ms / periode_ms   # ex: ≈ 2.0/16.67 ≈ 0.12
        
        normalized_angle = center_angle + (steering / 100.0) * range_deg
        
        duty_fraction = t_min_duty + (t_max_duty - t_min_duty) * (normalized_angle / 180.0)
        
        return int(duty_fraction * 65535)