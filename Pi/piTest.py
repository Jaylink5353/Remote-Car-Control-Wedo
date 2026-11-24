from piSocket import piSocketLib
import queue
import time

cmd_queue = queue.Queue()
socketServer = piSocketLib(command_queue=cmd_queue)

def Main():
    while True:
        time.sleep(0.01)

        try:
            command = cmd_queue.get_nowait()
            print("Incoming Command:" + command)

            if command == "tm":
                print("toggle")

            elif command == "w":
                print("forward")

            elif command == "s":
                print("back")

            elif command == "x":
                print("stop")

            elif command == "dc":
                print("disconnect")

        except queue.Empty:
            pass

Main()