# import threading
# import time
# import random


# class Process:
#     def __init__(self, process_id, total_processes):
#         self.id = process_id
#         self.total_processes = total_processes

#         # Lamport timestamp
#         self.timestamp = 0

#         # Whether this process is currently requesting the critical section
#         self.requested = False

#         # Number of replies received for the current request
#         self.reply_count = 0

#         # Lock to protect shared variables
#         self.lock = threading.Lock()

#         # Maximum number of times this process can request the CS
#         self.request_limit = 3

#         # Number of requests already made
#         self.request_count = 0

#     def request_critical_section(self):
#         """
#         Request access to the critical section.
#         """

#         if self.request_count >= self.request_limit:
#             print(
#                 f"Process {self.id} has reached its request limit "
#                 "and will terminate."
#             )
#             return

#         # Increment Lamport timestamp
#         self.timestamp += 1

#         self.requested = True
#         self.reply_count = 0

#         print(
#             f"Process {self.id} requesting critical section "
#             f"at timestamp {self.timestamp}."
#         )

#         # Send request to every other process
#         for i in range(self.total_processes):
#             if i != self.id:
#                 processes[i].receive_request(self.id, self.timestamp)

#         # Wait until replies from all other processes are received
#         while self.reply_count < self.total_processes - 1:
#             time.sleep(0.1)

#         # Enter the critical section
#         self.enter_critical_section()

#         # Count this request
#         self.request_count += 1

#     def receive_request(self, sender_id, sender_timestamp):
#         """
#         Handle a critical-section request received from another process.
#         """

#         with self.lock:

#             # If this process has a higher-priority request,
#             # it queues the incoming request.
#             if self.requested and self.timestamp < sender_timestamp:
#                 print(
#                     f"Process {self.id} queuing request from "
#                     f"Process {sender_id} at timestamp "
#                     f"{sender_timestamp}."
#                 )

#                 return

#             # Otherwise, send a reply immediately
#             print(f"Process {self.id} sending reply to " f"Process {sender_id}.")

#             processes[sender_id].receive_reply(self.id)

#     def receive_reply(self, sender_id):
#         """
#         Receive a reply from another process.
#         """

#         with self.lock:
#             self.reply_count += 1

#             print(f"Process {self.id} received reply from " f"Process {sender_id}.")

#     def enter_critical_section(self):
#         """
#         Simulate entering and executing the critical section.
#         """

#         print(f"Process {self.id} entering critical section.")

#         # Simulate work
#         time.sleep(random.uniform(1, 3))

#         print(f"Process {self.id} exiting critical section.")

#         self.release_critical_section()

#     def release_critical_section(self):
#         """
#         Release the critical section.
#         """

#         self.requested = False
#         self.reply_count = 0

#         print(f"Process {self.id} released critical section.")


# def process_runner(process):
#     """
#     Continuously make critical-section requests
#     until the request limit is reached.
#     """

#     while process.request_count < process.request_limit:

#         # Wait for a random amount of time before requesting
#         time.sleep(random.uniform(1, 2))

#         process.request_critical_section()


# # --------------------------------------------------
# # Main Program
# # --------------------------------------------------

# num_processes = 5

# # Create all processes
# processes = [Process(i, num_processes) for i in range(num_processes)]

# threads = []

# # Create and start a thread for every process
# for process in processes:

#     thread = threading.Thread(target=process_runner, args=(process,))

#     threads.append(thread)
#     thread.start()


# # Wait for all processes to finish
# for thread in threads:
#     thread.join()


# print("All processes have completed their requests.")

import threading
import queue
import time

N = 5


class Process(threading.Thread):
    def __init__(self, pid):
        super().__init__()

        self.pid = pid
        self.clock = 0

        # Message queue for this process
        self.messages = queue.Queue()

        # Request information
        self.requesting = False
        self.request_timestamp = None

        # Replies received
        self.replies_received = 0

        # Processes whose replies are being deferred
        self.deferred = set()

        self.lock = threading.Lock()

    def send(self, receiver, message):
        receiver.messages.put(message)

    def broadcast_request(self, processes):
        self.clock += 1

        self.request_timestamp = self.clock
        self.requesting = True
        self.replies_received = 0

        print(f"P{self.pid} REQUEST " f"(timestamp={self.request_timestamp})")

        # Send REQUEST to every other process
        for process in processes:
            if process.pid != self.pid:
                self.send(process, ("REQUEST", self.request_timestamp, self.pid))

    def receive_request(self, timestamp, sender_id, processes):
        # Update Lamport clock
        self.clock = max(self.clock, timestamp) + 1

        # If I am not requesting CS -> send REPLY
        if not self.requesting:

            print(f"P{self.pid} -> P{sender_id}: REPLY")

            self.send(processes[sender_id], ("REPLY", self.pid))

        else:

            # Compare requests:
            # smaller (timestamp, process_id) gets priority

            my_request = (self.request_timestamp, self.pid)

            sender_request = (timestamp, sender_id)

            if sender_request < my_request:

                print(f"P{self.pid} -> P{sender_id}: REPLY")

                self.send(processes[sender_id], ("REPLY", self.pid))

            else:

                print(f"P{self.pid} DEFERRED reply to P{sender_id}")

                self.deferred.add(sender_id)

    def receive_reply(self, sender_id):
        self.replies_received += 1

        print(f"P{self.pid} received REPLY from P{sender_id}")

    def enter_critical_section(self, processes):

        print(f"\n========== P{self.pid} ENTERED " f"CRITICAL SECTION ==========\n")

        time.sleep(2)

        print(f"\n========== P{self.pid} LEFT " f"CRITICAL SECTION ==========\n")

        # Finished requesting
        self.requesting = False
        self.request_timestamp = None

        # Send deferred replies
        for pid in self.deferred:

            print(f"P{self.pid} -> P{pid}: " f"DEFERRED REPLY")

            self.send(processes[pid], ("REPLY", self.pid))

        self.deferred.clear()

    def run(self):

        # Wait a little so all processes start
        time.sleep(1)

        # Each process requests CS at a different time
        time.sleep(self.pid * 0.5)

        # Request critical section
        self.broadcast_request(processes)

        # Keep processing messages
        while True:

            try:
                message = self.messages.get(timeout=0.1)

            except queue.Empty:
                continue

            if message[0] == "REQUEST":

                _, timestamp, sender_id = message

                self.receive_request(timestamp, sender_id, processes)

            elif message[0] == "REPLY":

                _, sender_id = message

                self.receive_reply(sender_id)

                # Received replies from everyone
                if self.replies_received == N - 1:

                    self.enter_critical_section(processes)

                    break


# Create 5 processes
processes = [Process(i) for i in range(N)]

# Start all processes
for process in processes:
    process.start()

# Wait for all processes to finish
for process in processes:
    process.join()

print("\nAll processes completed.")
