from threading import Lock


class Singleton (type):
    __instances = {}
    __singleton_lock = Lock()

    def __call__(cls, *args, **kwargs):
        with Singleton.__singleton_lock:
            if cls not in Singleton.__instances:
                Singleton.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            return Singleton.__instances[cls]

    def clear(cls):
        with Singleton.__singleton_lock:
            try:
                del Singleton.__instances[cls]
            except KeyError:
                pass
