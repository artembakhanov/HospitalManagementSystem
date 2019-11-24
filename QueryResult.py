def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls


@auto_str
class QueryResult:
    def __init__(self):
        self.column_names = None
        self.values = None
        self.is_error = False
        self.exception = None
