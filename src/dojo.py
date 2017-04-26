from .room import Room

class Dojo(object):
    """This class is responsible for managing and allocating rooms to people"""

    def __init__(self):
        self.all_rooms = []
        self.all_people = []

    def create_room(self, room_type, *room_names):
        created_rooms = []
        for room_name in room_names:
            room = Room(room_type, room_name)
            self.all_rooms.append(room)
            created_rooms.append(room)
            print("An {0} called {1} has been successfully created!".format(room_type, room_name))
        return created_rooms[0] if len(created_rooms) == 1 else created_rooms

    def add_person(self, first_name, last_name, person_type, wants_accomodation = "N"):
        rooms = []
        person_id = len(self.all_people) + 1
        person = Staff(first_name, last_name, person_type, person_id) if person_type == "Staff" else\
            Fellow(first_name, last_name, person_type, wants_accomodation, person_id)
        print("{0} {1} {2} has been successfully added".format(person_type, first_name, last_name))
        self.all_people.append(person)
        # Assign office to person
        office_rooms = [room for room in self.all_rooms if room.room_type == "office"]
        for office in office_rooms:
            if not office.fully_occupied:
                office.add_person_to_room(person)
                person.has_office = True
                rooms.append({"office": office.room_name})
                print("{0} has been allocated the office {1}".format(first_name, office.room_name))
                break
        if not person.has_office:
            print("Sorry, there are no more office rooms for {0} to occupy.".format(first_name))
