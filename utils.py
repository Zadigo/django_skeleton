class LazyObject:
    def __init__(self):
        self.container = None

    def __getattr__(self, name):
        if self.container is None:
            self._setup()
        value = getattr(self.container, name)
        self.__dict__[name] = value
        return value

    def _setup(self):
        pass
