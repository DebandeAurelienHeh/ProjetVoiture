# 🚗 LamboCar 6

**LamboCar 6** is a Python 3-based project developed using a Raspberry Pi (single-board computer), with the goal of building a mobile module capable of competing in a Formula 1-style race on a custom track defined by our teachers.

## 🎯 Project Goal

The project is intended for:
- Spectators of the annual **HEH Grand Prix**
- Automobile enthusiasts
- Race organizers and all stakeholders of the HEH Grand Prix

## 🛠️ Project Overview

Team 6 dedicated a full week of work to build this technological gem.

The **LamboCar** is equipped with:
- **Ultrasonic sensors** for obstacle avoidance and navigation
- **Servomotors** to take on curves efficiently
- **RGB sensor** for lightning-fast starts as soon as the light turns green
- **Infrared sensor** to increment lap counts when crossing the starting line

## 🧰 Technologies & Libraries

Our team used several Python libraries to properly manage the sensors and actuators:
- `RPi.GPIO`
- `Adafruit_PCA9685`
- `unittest`
- `unittest.mock`
- `busio`

## 🔧 Components Used

All components were provided or approved by our teachers:

| Component         | Description               |
|------------------|---------------------------|
| **HC-SR04**       | Ultrasonic sensor         |
| **TCRT5000**      | Infrared sensor           |
| **INA219**        | Current/voltage sensor    |
| **L298N**         | Dual H-bridge motor driver |
| **DC motor**      | Main propulsion           |
| **PCA9685**       | PWM controller            |
| **SG90**          | Servomotor for steering   |
| **PiJuice**       | Power management module   |
| **18650 Batteries** | Power supply            |

## 📚 Additional Documentation

- 📄 [Hardware Documentation (French)(PDF)](docs/ChoixMateriel.pdf)
- 📄 [Software and Libraries Choices (French)(PDF)](docs/DocumentationChoixLogiciels.pdf)


## 👥 Team 6 Members

- De Coster Koryan  
- Debande Aurélien  
- Duchenne Corentin  
- Isembaert Nathan  
- Kozlenko Anastasiia  
- Rousche Aurélien
