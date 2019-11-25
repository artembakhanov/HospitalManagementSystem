class QueryResult:
    def __init__(self):
        self.column_names = None
        self.values = None
        self.is_error = False
        self.exception = None

    def __str__(self):
        return f"QueryResult{{" \
               f"column_names={self.column_names}, " \
               f"values={self.values}, " \
               f"is_error={self.is_error}, " \
               f"exception={self.exception}}}"
