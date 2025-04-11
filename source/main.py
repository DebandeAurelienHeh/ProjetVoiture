import LamboCar
import busio
import board

def main():
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    lambo = LamboCar.LamboCar(i2c_bus)

    ack=True
    while ack:
        command = input("Enter mode here [test,start,green]")
        if command == "test":
            lambo.test()
            ack = False
        elif command == "start":
            tours = input("How many turns?")
            lambo.start(tours)
            ack = False
        elif command == "green":
            tours = input("How many turns?")
            lambo.start_on_green(tours)
            ack = False

if __name__ == "__main__":
    main()

