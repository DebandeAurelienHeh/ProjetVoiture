class ServoMotor():
    def __init__(self, boardChannel:int, rangeDegrees:int):
        self.__boardChannel = boardChannel
        self.__rangeDegrees = rangeDegrees
        self.__minPulse = 1.0 # in ms
        self.__maxPulse = 2.0 # in ms
        self.__centerAngle = 80
        self.__frequency = 50
    
    @property
    def boardChannel(self) -> int:
        return self.__boardChannel
    @property
    def rangeDegrees(self) -> float:
        return self.__rangeDegrees
    @property
    def minPulse(self) -> float:
        return self.__minPulse
    @property
    def maxPulse(self) -> float:
        return self.__maxPulse
    @property
    def centerAngle(self) -> float:
        return self.__centerAngle
    @property
    def frequency(self) -> float:
        return self.__frequency

    
    
    