class ILogger:
    """Logger interface."""
    def info(self, msg) -> None:
        """
        Write info message.
        """
        pass

    def warn(self, msg, ex=None) -> None:
        """
        Write warning message (with stacktrace if exception is passed).
        """
        pass

    def error(self, msg, ex=None) -> None:
        """
        Write error message (with stacktrace if exception is passed).
        """
        pass
