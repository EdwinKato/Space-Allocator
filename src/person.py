"""Class definition of class Person"""

from abc import ABCMeta, abstractmethod

class Person(object):
    """ This class is responsible for managing people's data """

    def __init__(self, first_name, last_name,\
        wants_accommodation, _id, has_living_space=None, has_office=None):
        self.first_name = first_name
        self.last_name = last_name
        self._id = _id
        self._type = None
        self.has_living_space = None if has_living_space is None else True
        self.has_office = None if has_office is None else True
        self.rooms_occupied = []
        self.wants_accommodation = wants_accommodation

    def get_fullname(self):
        """get_fullname()

        Returns:
            Fullname of person
        """

        return self.first_name + " " + self.last_name

    @abstractmethod
    def set_type(self):
        pass
