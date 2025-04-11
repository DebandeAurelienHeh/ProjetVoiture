class DistanceData:
    """
    Class to store the distance data from ultrasonic sensors.
    """
    def __init__(self, front, left, right):
        self.__front = front
        self.__left = left
        self.__right = right

    @property
    def front(self):
        return self.__front

    @property
    def left(self):
        return self.__left

    @property
    def right(self):
        return self.__right