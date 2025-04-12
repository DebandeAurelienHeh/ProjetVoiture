import LamboCar
import busio
import board

def main():
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    lambo = LamboCar.LamboCar(i2c_bus)

    ack=True
    while ack:
        command = input("Enter mode here [test,start,green,avoid,reverseGear,uTurn,eightTurn]")
        if command.lower() == "test":
            lambo.test()
            ack = False
        elif command.lower() == "start":
            tours = int(input("How many turns?"))
            lambo.start(tours)
            ack = False
        elif command.lower() == "green":
            tours = int(input("How many turns?"))
            lambo.start_on_green(tours)
            ack = False
        elif command.lower() == "avoid":
            lambo.zigzagAvoidance()
            ack = False
        elif command.lower() == "reversegear":
            lambo.reverseGear()
            ack = False
        elif command.lower() == "uturn":
            lambo.uTurn()
            ack = False
        elif command.lower() == "eightturn":
            lambo.eightTurn()
            ack = False


if __name__ == "__main__":
    main()

