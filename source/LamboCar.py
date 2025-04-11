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
        try:
            on_line = self.sensorManager.detectLine()
            if on_line and not self.__last_line_state:
                self.__tour += 1
                self.logger.info(f"Lap counted! Total laps: {self.__tour}")
            self.__last_line_state = on_line
        except Exception as e:
            self.logger.error(f"Error in LineCount: {e}")

    def stayMid(self):
        # Récupération et normalisation des distances
        distances = self.sensorManager.getDistance()

        # Clamp des valeurs selon les limites des capteurs (2cm - 400cm)
        frontDist = max(min(distances.front or 400, 400), 2)
        leftDist = max(min(distances.left or 400, 400), 2)
        rightDist = max(min(distances.right or 400, 400), 2)

        # Configuration des paramètres
        corridor_width = 60  # cm
        target_offset = 15  # cm de marge de chaque côté
        Kp = 3  # Gain proportionnel réduit
        base_speed = 30  # vitesse de base réduite
        min_front = 25  # distance frontale minimale

        # 1. Logique d'évitement d'obstacle frontal
        if frontDist < min_front:
            self.logger.info("Obstacle frontal détecté - Manœuvre d'évitement")
            self.__motorManager.setSpeed(-25)
            # Choix de la direction avec le plus d'espace
            if (leftDist - target_offset) > (rightDist - target_offset):
                self.__motorManager.setAngle(70)  # Recule à droite
            else:
                self.__motorManager.setAngle(-70)  # Recule à gauche
            time.sleep(0.8)
            self.__motorManager.setSpeed(base_speed)
            time.sleep(1.2)
            self.__motorManager.setAngle(0)
            return

        # 2. Calcul de la position idéale dans le couloir
        total_space = leftDist + rightDist
        if total_space < corridor_width * 0.8:  # Si le couloir semble rétrécir
            target_left = corridor_width / 2 - target_offset
            target_right = corridor_width / 2 - target_offset
        else:
            target_left = (corridor_width - (rightDist * 0.7))  # Priorité au côté droit dans les virages
            target_right = (corridor_width - (leftDist * 0.7))

        # 3. Calcul de l'erreur proportionnelle
        error = (rightDist - target_right) - (leftDist - target_left)
        angle = max(-70, min(70, Kp * error))

        # 4. Adaptation dynamique de la vitesse
        space_factor = min(frontDist / 100, 1.0)  # Réduction vitesse devant obstacle
        turn_factor = 1 - (abs(angle) / 70 * 0.4)  # Réduction en virage serré
        speed = max(20, base_speed * space_factor * turn_factor)

        # 5. Application des commandes
        self.__motorManager.setAngle(int(angle))
        self.__motorManager.setSpeed(int(speed))

        self.logger.debug(f"L:{leftDist:.1f} | R:{rightDist:.1f} | Ang:{angle:.1f} | Spd:{speed:.1f}")

        return (speed, angle)

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

    def prepareSensors(self):
        print("Preparing sensors...")
        all_ready = True

        # ---- RGB Sensor ----
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

        # ---- INA219 Current Sensor ----
        data_ina = self.__sensorManager.getCurrent()
        if data_ina is not None:
            print(f"Current in milliamps: {data_ina}")
            self.logger.info(f"INA219 sensor is ready. Current in milliamps: {data_ina}")
            print("INA219 sensor is ready!")
        else:
            print("INA219 sensor does not respond!")
            self.logger.error("INA219 sensor does not respond!")
            all_ready = False

        # ---- Distance Sensors ----
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

        # ---- Line Sensor ----
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
        while True:
            if self.__sensorManager.isGreen():
                self.logger.info("GREEN LIGHT! THE RACE IS ON!")
                self.start(tours)
            else:
                self.logger.info("NOT GREEN YET!")
                time.sleep(0.5)

    def stayMid(self):
        distance = self.__sensorManager.getDistance()
        frontDist = distance.front
        leftDist = distance.left
        rightDist = distance.right

        min_front = 20
        max_front = 100
        Kp = 10

        if frontDist is None or frontDist < min_front:
            self.__motorManager.setSpeed(-30)
            time.sleep(1)  # ça a été rajouté pour éviter que la voiture ne recule trop
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
            # Moteur n'avancerait pas avec la vitesse trop basse

        newSpeed = max(40, min(41, rawSpeed))
        correctionFactor = 1 - (abs(newAngle) / 100) * 0.5
        newSpeed *= correctionFactor

        self.__motorManager.setAngle(newAngle)
        self.__motorManager.setSpeed(newSpeed)

        return (newSpeed, newAngle)

    def test(self):
        self.prepareMotors()
        time.sleep(1)
        self.prepareSensors()
        time.sleep(1)
        self.start()

    def start(self, max_tours=1):
        line_detected = False
        try:
            while self.tour < max_tours:
                self.stayMid()
                if self.sensorManager.detectLine() and not line_detected:
                    self.tour+=1
                    line_detected = True
                elif not self.sensorManager.detectLine():
                    line_detected = False
                time.sleep(0.05)
            self.stopCar()
        except KeyboardInterrupt:
            print("Stop the car.")
            self.stopCar()


    """ 
       def start(self):
            try:
                while True:
                    self.stayMid()
                    time.sleep(0.05)
            except KeyboardInterrupt:
                print("Stop the car.")
                self.stopCar()
    """

"""
def main():
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
"""
