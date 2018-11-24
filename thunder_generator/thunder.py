"""Thunder generator class"""
from random import randint, uniform
from shapely.geometry import Point, Polygon


class Thunder:
    """Thunder direction simulator class."""
    __vector_random_range = (-0.45, 0.45)
    __boundaries_lat = (0, 0)
    __boundaries_lng = (0, 0)
    __just_created = True
    __vector_life = 8
    __vector = {
        'lng': 0.0,
        'lat': 0.0
    }

    def __init__(self, id, lng, lat, borders):
        self.__id = id
        self.__lng = lng
        self.__lat = lat
        self.__borders = Polygon(borders)

    @property
    def id(self):
        return self.__id

    def get_next_coordinates(self):
        if self.__just_created:
            self.__calculate_vector()
            self.__just_created = False
        return self.__calculate_coordinates()

    def __calculate_coordinates(self):
        if self.__vector_life > 0:
            self.__vector_life -= 1
        else:
            self.__vector_life = 30
            self.__calculate_vector()
        self.__lng += self.__vector['lng']
        self.__lat += self.__vector['lat']
        point = Point( self.__lng, self.__lat)
        inside_borders = point.within(self.__borders)
        if not inside_borders:
            self.__reverse_vector_direction()
        return self.__id, self.__lng, self.__lat


    def __calculate_vector(self):
        self.__vector['lng'] = uniform(*self.__vector_random_range)
        self.__vector['lat'] = uniform(*self.__vector_random_range)

    def __reverse_vector_direction(self):
        self.__vector_life = 30
        self.__vector['lng'] = -self.__vector['lng']
        self.__vector['lat'] = -self.__vector['lat']
