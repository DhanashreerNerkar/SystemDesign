from abc import ABC, abstractmethod
from collections import deque

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    @abstractmethod
    def undo(self):
        pass

class SendWelcomeEmailCommand(Command):
    def __init__(self, patient_id):
        self.patient_id = patient_id
    def execute(self):
        print(f"[Email] Welcome email sent to patient {self.patient_id}")
    def undo(self):
        print(f"[Email] Cannot unsend email for {self.patient_id}")

class SyncWearableDataCommand(Command):
    def __init__(self, patient_id):
        self.patient_id = patient_id
    def execute(self):
        print(f"[Wearable] Syncing Apple Health data for {self.patient_id}")
    def undo(self):
        print(f"[Wearable] Removing synced data for {self.patient_id}")

class RunPredictionModelCommand(Command):
    def __init__(self, patient_id):
        self.patient_id = patient_id
    def execute(self):
        print(f"[Model] Generating baseline risk score for {self.patient_id}")
    def undo(self):
        print(f"[Model] Discarding risk score for {self.patient_id}")

# Invoker: a simple task queue that runs and logs commands, supports retry
class RegistrationTaskQueue:
    def __init__(self):
        self._queue = deque()
        self._history = []

    def add_command(self, command: Command):
        self._queue.append(command)

    def run_all(self):
        while self._queue:
            command = self._queue.popleft()
            try:
                command.execute()
                self._history.append(command)
            except Exception as e:
                print(f"[Retry] {command.__class__.__name__} failed: {e} — re-queuing")
                self._queue.append(command)

    def undo_last(self):
        if self._history:
            self._history.pop().undo()

# Usage
queue = RegistrationTaskQueue()
patient_id = "P-2001"
queue.add_command(SendWelcomeEmailCommand(patient_id))
queue.add_command(SyncWearableDataCommand(patient_id))
queue.add_command(RunPredictionModelCommand(patient_id))
queue.run_all()
queue.undo_last()  # e.g., patient withdrew consent right after registering