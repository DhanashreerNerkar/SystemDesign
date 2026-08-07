# Example: Easy
class DataProcessor:
    def process(self, data):
        return data  # base: just passes patient demographic data through

class EncryptionDecorator:
    def __init__(self, wrapped):
        self.wrapped = wrapped
    def process(self, data):
        data = self.wrapped.process(data)
        return f"ENCRYPTED({data})"

class LoggingDecorator:
    def __init__(self, wrapped):
        self.wrapped = wrapped
    def process(self, data):
        print(f"Logging: processing patient record")
        return self.wrapped.process(data)

# Stack decorators dynamically
pipeline = LoggingDecorator(EncryptionDecorator(DataProcessor()))
print(pipeline.process("patient_demographics"))