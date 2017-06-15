"""Class definition of LivingSpace"""

from .room import Room

class LivingSpace(Room):
    """LivingSpace"""

    def __init__(self, name):
        super(LivingSpace, self).__init__(name)
        self.maximum_no_of_people = 4
        self.set_type()

    def set_type(self):
        self._type = "living_space"
