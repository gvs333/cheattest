from abc import abstractmethod, ABC


class BaseCommand(ABC):

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def do(self):
        pass
