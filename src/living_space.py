"""Class definition of LivingSpace"""

from .room import Room

class LivingSpace(Room):
    """LivingSpace"""

    def __init__(self, room_name):
        super(LivingSpace, self).__init__("living_space", room_name)

