from .room import Room


class Office(Room):

    def __init__(self, room_type, room_name):
        super(Office, self).__init__(room_type, room_name)

