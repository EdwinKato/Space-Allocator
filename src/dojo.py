from .room import Room

class Dojo(object):
    """This class is responsible for managing and allocating rooms to people"""

    def __init__(self):
        self.all_rooms = []
        self.all_people = []

    def create_room(self, room_type, *room_names):
        created_rooms = []
        for room_name in room_names:
            if room_name not in [room.room_name for room in self.all_rooms]:
                room = Office(room_type, room_name) if room_type == "office" else LivingSpace(room_type, room_name)
                self.all_rooms.append(room)
                created_rooms.append(room)
                print("An {0} called {1} has been successfully created!".format(room_type, room_name))
            else:
                print("Room with name: {0} already exists. Please try using another name".format(room_name))
        return created_rooms[0] if len(created_rooms) == 1 else created_rooms


