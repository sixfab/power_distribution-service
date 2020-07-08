class RetryLimitError(Exception):
    def __init__(self):
        super().__init__("Exceeded retry limit")