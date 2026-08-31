import threading
import queue
import time

N = 5


class Process(threading.Thread):
    def __init__(self, pid):
        super().__init__()

        self.pid = pid
        self.messages = queue.Queue()
        self.requesting = False

    def send(self, receiver, message):
        receiver.messages.put(message)

    def enter_critical_section(self):
        print(f"P{self.pid} ENTERED CRITICAL SECTION")

        time.sleep(2)

        print(f"P{self.pid} LEFT CRITICAL SECTION")

    def run(self):
        time.sleep(self.pid * 0.5)

        self.requesting = True
        print(f"P{self.pid} REQUESTED CRITICAL SECTION")

        while True:
            message = self.messages.get()

            if message == "TOKEN":
                if self.requesting:
                    self.enter_critical_section()
                    self.requesting = False

                next_pid = (self.pid + 1) % N
                processes[next_pid].messages.put("TOKEN")
                break


processes = [Process(i) for i in range(N)]

for process in processes:
    process.start()

# Initially give the token to P0
processes[0].messages.put("TOKEN")

for process in processes:
    process.join()

print("All processes completed.")