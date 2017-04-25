class Room(object):
    """ This class is responsible for managing the people in a room """

    def __init__(self, room_type, room_name):
        self.residents = []
        self.room_name = room_name
        self.room_type =room_type
        if room_type == "office":
            self.maximum_no_of_people = 6
        else:
            self.maximum_no_of_people = 4

