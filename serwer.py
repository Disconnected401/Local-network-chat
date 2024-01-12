import socket
import threading
import time
from colorama import Fore

W = Fore.WHITE
G = Fore.LIGHTGREEN_EX
R = Fore.LIGHTRED_EX


def print_gradient_text(text, start_color, end_color):
    num_steps = len(text)
    for i in range(num_steps):
        ratio = i / (num_steps - 1)
        color = (
            int(start_color[0] + (end_color[0] - start_color[0]) * ratio),
            int(start_color[1] + (end_color[1] - start_color[1]) * ratio),
            int(start_color[2] + (end_color[2] - start_color[2]) * ratio),
        )
        gradient_color = f"\033[38;2;{color[0]};{color[1]};{color[2]}m"
        print(f"{gradient_color}{text[i]}", end="", flush=True)
        time.sleep(0.0001)
    print("\033[0m")


start_color = (255, 0, 0)

end_color = (255, 111, 0)

logo_text = r"""
,--.  ,--.,--.   ,--.   ,--.                    ,---.                                        
|  '--'  |`--' ,-|  | ,-|  | ,---. ,--,--,     '   .-'  ,---. ,--.--.,--.  ,--.,---. ,--.--. 
|  .--.  |,--.' .-. |' .-. || .-. :|      \    `.  `-. | .-. :|  .--' \  `'  /| .-. :|  .--' 
|  |  |  ||  |\ `-' |\ `-' |\   --.|  ||  |    .-'    |\   --.|  |     \    / \   --.|  |    
`--'  `--'`--' `---'  `---'  `----'`--''--'    `-----'  `----'`--'      `--'   `----'`--'
"""

print_gradient_text(logo_text, start_color, end_color)

active_connections = []

def handle_client(client_socket, addr):
    try:
        print(f"{addr[0]} - {addr[1]} >>> {G}connected{W}")

        active_connections.append(client_socket)

        while True:
            data = client_socket.recv(1024).decode('utf-8')

            if not data:
                break

            for connection in active_connections:
                if connection != client_socket:
                    connection.send(f"{addr[0]} >>> {data}".encode('utf-8'))

    except Exception as e:
        print()

    finally:
        active_connections.remove(client_socket)

        print(f"{addr[0]} - {addr[1]} >>> {R}disconnected{W}")

        client_socket.close()

def start_server():
    host = '192.168.100.107'
    port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()

            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_handler.start()

    except KeyboardInterrupt:
        print("Server shutting down.")
        server_socket.close()

if __name__ == "__main__":
    start_server()