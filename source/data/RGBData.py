class RGBData:
    """
    RGBData class to represent RGB color values.
    Attributes:
        red (int): Red color value.
        green (int): Green color value.
        blue (int): Blue color value.
    """
    def __init__(self, red, green, blue):
        self.__red = red
        self.__green = green
        self.__blue = blue

    @property
    def red(self):
        return self.__red

    @property
    def green(self):
        return self.__green

    @property
    def blue(self):
        return self.__blue