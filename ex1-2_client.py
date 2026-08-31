import socket
import pickle


class DataObject:
    def __init__(self, name, values):
        self.name = name
        self.values = values


HOST = "127.0.0.1"
PORT = 5001
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
obj = DataObject("John", [100, 200, 300, 400])
serialized = pickle.dumps(obj)
client.send(serialized)
response = client.recv(1024).decode()
print(response)
client.close()
