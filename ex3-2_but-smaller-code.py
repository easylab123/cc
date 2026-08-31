import threading
import time

N = 3


class Process(threading.Thread):
    def __init__(self, pid):
        super().__init__()
        self.pid = pid
        self.clock = 0
        self.request = None
        self.replies = 0
        self.deferred = []

    def request_cs(self):
        self.clock += 1
        self.request = (self.clock, self.pid)
        self.replies = 0

        print(f"P{self.pid} REQUEST {self.request}")

        for p in processes:
            if p.pid != self.pid:
                p.receive_request(self.request, self.pid)

        while self.replies < N - 1:
            time.sleep(0.1)

        self.enter_cs()

    def receive_request(self, request, sender):
        self.clock = max(self.clock, request[0]) + 1

        if self.request is None or request < self.request:
            print(f"P{self.pid} -> P{sender}: REPLY")
            processes[sender].receive_reply(self.pid)
        else:
            print(f"P{self.pid} deferred P{sender}")
            self.deferred.append(sender)

    def receive_reply(self, sender):
        self.replies += 1
        print(f"P{self.pid} received REPLY from P{sender}")

    def enter_cs(self):
        print(f"P{self.pid} ENTERED CRITICAL SECTION")
        time.sleep(2)
        print(f"P{self.pid} LEFT CRITICAL SECTION")

        self.request = None

        for pid in self.deferred:
            print(f"P{self.pid} -> P{pid}: REPLY")
            processes[pid].receive_reply(self.pid)

        self.deferred.clear()

    def run(self):
        time.sleep(self.pid * 0.5)
        self.request_cs()


processes = [Process(i) for i in range(N)]

for p in processes:
    p.start()

for p in processes:
    p.join()

print("All processes completed.")
