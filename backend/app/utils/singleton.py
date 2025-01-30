from threading import Lock


class Singleton (type):
    __instances = {}
    __singleton_lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls.__singleton_lock:
            if cls not in cls.__instances:
                cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls.__instances[cls]
