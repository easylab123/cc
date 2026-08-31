import threading
import socket


def thread_handler(client_socket, addr):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message or message.lower().strip() == "exit":
                print(f"Connection closed by {addr}")
                break
            print(f"Message from {addr}: {message}")
            response = input("Enter response: ")
            client_socket.send(response.encode())
        except Exception as e:
            print(f"Error: {e}")
            break
    print(f"Closing connection with {addr}")
    client_socket.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 12345))
server.listen()
print("Server listening on port 12345...")

while True:
    client_socket, addr = server.accept()
    print(f"Connection established with {addr}")
    thread = threading.Thread(target=thread_handler, args=(client_socket, addr))
    thread.start()
