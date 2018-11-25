"""Thunder generator class"""
from random import randint, uniform
from shapely.geometry import Point, Polygon
import math
import numpy as np


class Thunder:
    """Thunder direction simulator class."""
    __vector_random_range = (-0.099, 0.099)
    __boundaries_lat = (0, 0)
    __boundaries_lng = (0, 0)
    __just_created = True
    __vector_life = None
    __vector = {
        'lat': 0.0,
        'lng': 0.0
    }

    def __init__(self, id, lat, lng, borders):
        self.__id = id
        self.__lat = lat
        self.__lng = lng
        self.__borders = Polygon(borders)
        self.__vector_life = randint(5, 10)

    @property
    def id(self):
        return self.__id

    def get_next_coordinates(self):
        """Get next lng and lat coordinates of thunder position."""
        if self.__just_created:
            self.__calculate_vector()
            self.__just_created = False
        return self.__calculate_coordinates()

    def __calculate_coordinates(self):
        """Calculate coordinates based on life vector."""
        if self.__vector_life > 0:
            self.__vector_life -= 1
        else:
            self.__vector_life = randint(5, 10)
            # self.__rotate_around_last_coordinates()
            self.__calculate_vector()
        self.__lat += self.__vector['lat']
        self.__lng += self.__vector['lng']
        point = Point(self.__lat, self.__lng)
        inside_borders = point.within(self.__borders)
        if not inside_borders:
            self.__reverse_vector_direction()
        print(self.__vector)
        return self.__id, self.__lat, self.__lng

    def __calculate_vector(self):
        """Calculate vector for given life."""
        self.__vector['lat'] = uniform(*self.__vector_random_range)
        self.__vector['lng'] = uniform(*self.__vector_random_range)

    def __reverse_vector_direction(self):
        """Reverse vector direction and recalculate life."""
        self.__vector_life = randint(5, 10)
        self.__vector['lat'] = -self.__vector['lat']
        self.__vector['lng'] = -self.__vector['lng']

    def __rotate_around_last_coordinates(self):
        """Rotate a point around a last coordinates."""
        degrees = randint(-30, 30)
        radians = math.radians(degrees)
        x, y = self.__lat, self.__lng
        offset_x, offset_y = self.__lat - self.__vector['lat'], self.__lng - self.__vector['lng']
        adjusted_x = (x - offset_x)
        adjusted_y = (y - offset_y)
        cos_rad = math.cos(radians)
        sin_rad = math.sin(radians)
        self.__vector['lat'] = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
        self.__vector['lng'] = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
