"""Class definition of Office

"""
from .room import Room

class Office(Room):
    """Office
    Office inherits from the Room class
    """

    def __init__(self, room_name):
        super(Office, self).__init__("office", room_name)

