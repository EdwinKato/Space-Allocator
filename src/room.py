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

    def get_residents(self):
        """ Get people in room

        Returns:
            Array of names of the people in the room

        """

        people = []
        for person in self.residents:
            people.append(person.get_fullname())
        return people

    def remove_person(self, person):
        """Removes a person from a room

        Args:
            person (Person): Person to be removed from the room

        Returns:
            True if successful, False otherwise.
        """

        if person in self.residents:
            self.residents.remove(person)
            if self.fully_occupied:
                self.fully_occupied = None
            return True
        else:
            return False

    @abstractmethod
    def set_type(self):
        pass
