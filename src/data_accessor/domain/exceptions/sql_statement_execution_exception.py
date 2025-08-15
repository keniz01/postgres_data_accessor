class SqlStatementExecutionException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __repr__(self):
        return f"{self.__class__.__name__} [{self.message}]"