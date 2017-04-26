class Room(object):
    """ This class is responsible for managing the people in a room """

    def __init__(self, room_type, room_name):
        self.residents = []
        self.room_name = room_name
        self.room_type =room_type
        self.fully_occupied = None

        if room_type == "office":
            self.maximum_no_of_people = 6
        else:
            self.maximum_no_of_people = 4

    def add_person_to_room(self, person):
        if len(self.residents) != self.maximum_no_of_people:
            self.residents.append(person)
            if len(self.residents) == self.maximum_no_of_people: self.fully_occupied = True

    def get_people_in_room(self):
        people = []
        for person in self.residents:
            people.append(person.get_fullname())
        return people

    def remove_person_from_room(self, person):
        if person in self.residents: self.residents.remove(person)
        if self.fully_occupied: self.fully_occupied = None