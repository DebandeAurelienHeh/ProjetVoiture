from abc import ABC
from abc import abstractmethod

""" Interface Sensor """
class Sensor(ABC):
    @abstractmethod
    def readValue() -> any:
        pass