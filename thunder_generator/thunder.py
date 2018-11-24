"""Thunder generator class"""


class Thunder:
    """Thunder simulator class."""
    __coordinates = {
        lng: None
        lat: None
    }
    __gradient_map = []

    def __init__(self, start_coordinates coordinates_range,
        start_size, max_size, min_size, longevity, gradient_size):
        self.__coordinates = start_coordinates
        self.__coordinates_range = coordinates_range
        self.__max_size = max_size
        self.__min_size = min_size
        self.__size = min_size
        self.__longevity = longevity
        self.__gradient_size = gradient_size

    def generate_next(self):
