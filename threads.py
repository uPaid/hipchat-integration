from threading import Thread


class SimpleThread(Thread):
    def __init__(self, target, *args, **kwargs):
        self.__target = target
        self.__args = args
        self.__kwargs = kwargs
        Thread.__init__(self)

    def run(self):
        self.__target(*self.__args, **self.__kwargs)


def async(method):
    def __threaded(*args, **kwargs):
        SimpleThread(method, *args, **kwargs).start()

    return __threaded
