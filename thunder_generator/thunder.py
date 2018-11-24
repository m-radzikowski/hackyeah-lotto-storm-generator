"""Thunder generator class"""
from random import randint


class Thunder:
    """Thunder simulator class."""
    __coordinates = {
        'lng': None,
        'lat': None
    }
    __radius_steps = []
    __thunder_size = None
    __gradients_number = 3
    __growth = 10
    __rand_range = (0, 10)

    def __init__(self, start_coordinates, coordinates_range, min_size, max_size,
        gradient_size, longevity):
        self.__coordinates = start_coordinates
        self.__coordinates_range = coordinates_range
        self.__min_size = min_size
        self.__max_size = max_size
        self.__thunder_size = min_size + self.__growth
        self.__longevity = longevity

    def generate(self):
        if len(self.__radius_steps) == 0:
            return self.__generate_gradient()
        else:
            self.__calculate_scalar()
            self.__calculate_thunder_size()
            return self.__generate_gradient()

    def __generate_gradient(self):
        self.__radius_steps = []
        gradient_start = self.__thunder_size // self.__gradients_number
        gradient = 0
        for _ in range(self.__gradients_number):
            gradient += gradient_start
            self.__radius_steps.append(gradient)
        return self.__radius_steps

    def __calculate_scalar(self):
        if self.__thunder_size >= self.__max_size:
            self.__growth = -10
            self.__rand_range = (-10, 2)
        elif self.__thunder_size <= self.__min_size:
            self.__growth = 10
            self.__rand_range = (-2, 10)
        else:
            self.__growth = randint(*self.__rand_range)

    def __calculate_thunder_size(self):
        self.__thunder_size += self.__growth
        self.__thunder_size = self.__thunder_size if self.__thunder_size > self.__min_size else self.__min_size
        self.__thunder_size = self.__thunder_size if self.__thunder_size < self.__max_size else self.__max_size

    def __calculate_coordinates(self):
        
