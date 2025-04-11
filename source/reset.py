import sys
import time
import logging
import busio
import board
from LamboCar import LamboCar


def main():
    # Initialiser la voiture
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    lambo = LamboCar(i2c_bus)

    # On regarde s'il y a un argument en ligne de commande
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "stop":
            # Appel immédiat de la méthode stopCar
            lambo.stopCar()
            print(">>> Car stopped !")
            
        elif command == "reset":
            # S’il y a une logique de reset à ajouter, tu la mets ici
            print(">>> Resetting car...")
            # Par exemple :
            lambo.stopCar()
            # lambo.prepareMotors() ou autre...
            
        else:
            print(f"unknown command : {command}")
            print("Possible usage: python my_script.py stop | reset")
    else:
        print("No command specified.")
        print("Usage:")
        print("  python my_script.py stop")
        print("  python my_script.py reset")

# Point d'entrée
if __name__ == "__main__":
    main()