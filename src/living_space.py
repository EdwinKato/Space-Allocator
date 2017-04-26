from .room import Room


class LivingSpace(Room):

    def __init__(self, room_type, room_name):
        super(LivingSpace, self).__init__(room_type, room_name)

