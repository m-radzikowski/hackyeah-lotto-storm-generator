"""Thunder generator class"""
import random
from shapely.geometry import Point, Polygon
import math
import numpy as np


class Thunder:
    """Thunder direction simulator class."""
    __boundaries_lat = (0, 0)
    __boundaries_lng = (0, 0)
    __vector_life = None
    # __vector = {
    #     'lat': 0.0,
    #     'lng': 0.0
    # }

    def __init__(self, id, lat, lng, borders, vector_life, vector):
        self.__id = id
        self.__lat = lat
        self.__lng = lng
        self.__borders = Polygon(borders)
        self.__vector_life = vector_life

        self.__vector = {
            'lat': 0.0,
            'lng': 0.0
        }
        self.__vector_lat, self.__vector_lng = vector['lat'], vector['lng']

    @property
    def id(self):
        return self.__id

    def get_next_coordinates(self):
        """Get next lng and lat coordinates of thunder position."""
        return self.__calculate_coordinates()

    def __calculate_coordinates(self):
        """Calculate coordinates based on life vector."""
        if self.__vector_life > 0:
            self.__vector_life -= 1
        else:
            self.__vector_life = random.randint(5, 10)
            self.__recalculate_vector()
        self.__lat += self.__vector_lat
        self.__lng += self.__vector_lng
        point = Point(self.__lng, self.__lat) # needs to be in revers sequance for geojson list
        inside_borders = point.within(self.__borders)
        if not inside_borders:
            self.__reverse_vector_direction()
        return self.__id, self.__lat, self.__lng

    def __reverse_vector_direction(self):
        """Reverse vector direction and recalculate life."""
        self.__vector_life = random.randint(5, 10)
        self.__vector_lat = -self.__vector_lat
        self.__vector_lng = -self.__vector_lng

    def __recalculate_vector(self):
        """Change vector direction."""
        # radians = random.uniform(-0.2, 0.2)
        print('Vector before recalculated has lat {} lng{}'.format(self.__vector_lat, self.__vector_lng))
        # x, y = self.__lat, self.__lng
        # offset_x, offset_y = self.__lat - self.__vector_lat, self.__lng - self.__vector_lng
        # adjusted_x = (x - offset_x)
        # adjusted_y = (y - offset_y)
        # cos_rad = math.cos(radians)
        # sin_rad = math.sin(radians)
        # self.__vector_lat = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
        # self.__vector_lng = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
        self.__vector_lat = random.uniform(-0.059, 0.059)
        self.__vector_lng = random.uniform(-0.059, 0.059)
        print('Vector after recalculated to lat {} lng {}'.format(self.__vector_lat, self.__vector_lng))
