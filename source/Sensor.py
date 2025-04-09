from abc import ABC
from abc import abstractmethod

class Sensor(ABC):
    @abstractmethod
    def readValue() -> any:
        pass