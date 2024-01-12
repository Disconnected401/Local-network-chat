import time
import socket
import threading
import subprocess
import requests


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
        time.sleep(0.001)
    print("\033[0m")


start_color = (175, 175, 175)
end_color = (45, 45, 45)

logo_text = r"""                                                                                     
______ _            _      _    _       _ _ 
| ___ \ |          | |    | |  | |     | | |
| |_/ / | __ _  ___| | __ | |  | | __ _| | |
| ___ \ |/ _` |/ __| |/ / | |/\| |/ _` | | |
| |_/ / | (_| | (__|   <  \  /\  / (_| | | |
\____/|_|\__,_|\___|_|\_\  \/  \/ \__,_|_|_|
"""

print_gradient_text(logo_text, start_color, end_color)

def send_message(client_socket, hostname):
    try:
        while True:
            message = input()

            client_socket.send(f"{hostname} >>> {message}".encode('utf-8'))

    except Exception as e:
        if "10054" in str(e):
            print(f"Server closed the connection. {hostname} >>> disconnected")
        else:
            print(f"Error: {e}")

def receive_messages(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')

            if not data:
                break

            print(data.split(" >>> ", 1)[1])

    except Exception as e:
        if "10054" in str(e):
            print("Server closed the connection. Disconnected.")
        else:
            print(f"Error: {e}")

def start_client():
    host = '192.168.100.107'
    port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))

        hostname = socket.gethostname()

        print(f"connected to the server")

        send_thread = threading.Thread(target=send_message, args=(client_socket, hostname))
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))

        send_thread.start()
        receive_thread.start()

        send_thread.join()
        receive_thread.join()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()