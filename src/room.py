"""Room

This class is responsible for managing people in a room.
Example:
    To create a new instance, use
        room = Room()

Attributes:
    residents (Person[]): People currently leaving in the room
    name (str): Name of room.
    _type (str): Type of room ie Office / LivingSpace
    fully_occupied : True indicates that the room is occupied to capacity
"""

from abc import ABCMeta, abstractmethod


class Room(metaclass=ABCMeta):
    """ This class is responsible for managing the people in a room """

    def __init__(self, name):
        self.residents = []
        self.name = name
        self._type = None
        self.fully_occupied = None

    @abstractmethod
    def set_type(self):
        pass
