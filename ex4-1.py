class LamportClock:
    def __init__(self, process_id):
        self.process_id = process_id
        self.clock = 0

    def event(self):
        self.clock += 1
        print(f"Process {self.process_id} - Internal event with Timestamp {self.clock}")

    def send_message(self, receiver):
        self.clock += 1
        print(
            f"Process {self.process_id} sends a message to Process {receiver.process_id} with Timestamp {self.clock}"
        )
        receiver.receive_message(self.process_id, self.clock)

    def receive_message(self, sender_id, sender_timestamp):
        self.clock = max(self.clock, sender_timestamp) + 1
        print(
            f"Process {self.process_id} received a message from Process {sender_id} with updated Timestamp {self.clock}"
        )


process1 = LamportClock(1)
process2 = LamportClock(2)
process1.event()
process1.send_message(process2)
process2.event()
process2.send_message(process1)
