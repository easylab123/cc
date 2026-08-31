import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((socket.gethostname(), 12345))

print("Connected to the server. Type 'exit' to disconnect.")

while True:
    try:
        message = input("Enter message: ")
        client_socket.send(message.encode())

        if message.lower().strip() == "exit":
            print("Closing connection")
            break

        response = client_socket.recv(1024).decode()
        print(f"Message received: {response}")

    except Exception as e:
        print(f"Error: {e}")

client_socket.close()
