#PC Main Script
# Jaylink5353 on 11/23/26, some stuff taken from webview_app_test of Jaylink5353/TuringProject

from tkinter import Tk
import sys
import os
import socket
from pynput import keyboard

if sys.platform.startswith("linux"):
    os.environ["GDK_BACKEND"] = "x11"

client_socket = None
pressed_keys = set()
target_ip = None

class InputHandler:
    def on_press(self, key):
        try:
            k = key.char
            print(f"press {k}")
            k = k.lower()

            if k in ('w', 's') and k not in pressed_keys:
                pressed_keys.add(k)
                send_packet(k)
            elif k in ('p', 'o') and k not in pressed_keys:
                pressed_keys.add(k)
                send_packet(k)

        except AttributeError:
            pass

    def on_release(self, key):
        try:
            k = key.char
            try:
                k = key.char.lower()
            except AttributeError:
                return

            if k in ('w', 's', 'p', 'o'):
                pressed_keys.discard(k)
                if k in ('w', 's'):
                    remaining = pressed_keys.intersection(('w', 's'))
                    if remaining:
                        send_packet(next(iter(remaining)))
                    else:
                        send_packet("x")
        except AttributeError:
            pass

    def __init__(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        )
        self.listener.start()

    def stop(self):
        self.listener.stop()

def init_socket(ip):
    global client_socket, target_ip
    target_ip = ip
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(10)
        client_socket.sendto(b"PING", (ip, 5001))
        reply, _ = client_socket.recvfrom(1024)
        print("UDP test passed")
    except socket.timeout:
        print("No Reply!")
        print("Connection failed")
        sys.exit(1)

def send_packet(data_string):
    global client_socket
    if client_socket is None:
        init_socket(target_ip)
    if client_socket:
        try:
            client_socket.sendto(data_string.encode("utf-8"), (target_ip, 5001))
        except Exception as e:
            print("Packet send failed")
            client_socket = None
            init_socket(target_ip)

def main():
    ip = input("Target IP: ")
    if not ip:
        print("Put in IP")
        sys.exit(1)
    if ip == 'q':
        sys.exit(0)

    init_socket(ip)

    root = Tk()
    root.title("Keyboard listener")
    root.geometry("400x300")

    handler = InputHandler()

    def close():
        send_packet("x")
        handler.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", close)
    root.mainloop()




if __name__ == "__main__":
    main()