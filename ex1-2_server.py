import socket
import pickle


class DataObject:
    def __init__(self, name, values):
        self.name = name
        self.values = values


HOST = "127.0.0.1"
PORT = 5001
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for client...")
conn, addr = server.accept()
data = conn.recv(4096)
obj = pickle.loads(data)
print("Name:", obj.name)
print("Values:", obj.values)
total = sum(obj.values)
response = f"Hello {obj.name}, Sum = {total}"
conn.send(response.encode())
conn.close()
server.close()
