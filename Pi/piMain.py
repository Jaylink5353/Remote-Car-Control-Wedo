#Raspberry Pi Main Script:
# Jaylink5353 on 11/23/2026
import queue
import time
from threading import Thread
from wedo_fork import WeDo
from piSocket import piSocketLib

motor = "a"
wd = WeDo()
cmd_queue = queue.Queue()
socketServer = piSocketLib(command_queue=cmd_queue)


def toggleMotors():
    global motor
    if motor == "a":
        motor = "b"
    elif motor == "b":
        motor = "a"

def Main():
    Thread(target=socketServer.listen, daemon=True).start()

    while True:
        time.sleep(0.01)

        try:
            command = cmd_queue.get_nowait()
            print("Incoming Command:" + command)

            if command == "tm":
                toggleMotors()
            elif command == "w":
                if motor == "a":
                    wd.motor_a = 100
                elif motor == "b":
                    wd.motor_b = 100

            elif command == "s":
                if motor == "a":
                    wd.motor_a = -100
                elif motor == "b":
                    wd.motor_b = -100
            elif command == "x":
                wd.motor_a = 0
                wd.motor_b = 0

            elif command == "dc":
                break

        except queue.Empty:
            pass

    wd.motor_a = 0
    wd.motor_b = 0

Main()