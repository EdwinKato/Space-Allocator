"""Class definition of Office

"""
from .room import Room

class Office(Room):
    """Office
    Office inherits from the Room class
    """

    def __init__(self, name):
        super(Office, self).__init__(name)
        self.maximum_no_of_people = 6
        self.set_type()

    def set_type(self):
        self._type = "office"
