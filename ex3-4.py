import threading
import queue
import time

N = 5
COORDINATOR = 0


class Process(threading.Thread):
    def __init__(self, pid):
        super().__init__()

        self.pid = pid
        self.messages = queue.Queue()

    def send(self, receiver, message):
        receiver.messages.put((message, self.pid))

    def enter_critical_section(self):
        print(f"P{self.pid} ENTERED CRITICAL SECTION")

        time.sleep(2)

        print(f"P{self.pid} LEFT CRITICAL SECTION")

    def run(self):
        time.sleep(self.pid * 0.5)

        print(f"P{self.pid} REQUESTED CRITICAL SECTION")

        self.send(processes[COORDINATOR], "REQUEST")

        while True:
            message, sender = self.messages.get()

            if message == "GRANT":
                self.enter_critical_section()

                self.send(processes[COORDINATOR], "RELEASE")
                break


class Coordinator(Process):
    def __init__(self, pid):
        super().__init__(pid)

        self.queue = []
        self.busy = False

    def run(self):
        completed = 0

        while completed < N:
            message, sender = self.messages.get()

            if message == "REQUEST":
                self.queue.append(sender)

                if not self.busy:
                    self.grant_next()

            elif message == "RELEASE":
                self.busy = False
                completed += 1

                if self.queue:
                    self.grant_next()

    def grant_next(self):
        pid = self.queue.pop(0)

        self.busy = True

        print(f"Coordinator -> P{pid}: GRANT")

        self.send(processes[pid], "GRANT")


processes = [None] * N

processes[COORDINATOR] = Coordinator(COORDINATOR)

for i in range(1, N):
    processes[i] = Process(i)

for process in processes:
    process.start()

for process in processes:
    process.join()

print("All processes completed.")