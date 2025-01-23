from threading import Lock


class Singleton:
    """
    Base class for a class which will only ever be instantiated once.
    """
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                cls._instance = cls._instance or super().__new__(cls, *args, **kwargs)
        return cls._instance
