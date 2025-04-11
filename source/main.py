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
            lambo.start()
            ack = False
        elif command == "green":
            lambo.start_on_green()
            ack = False

