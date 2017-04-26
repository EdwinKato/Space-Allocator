from .living_space import LivingSpace
from .office import Office
from .fellow import Fellow
from .staff import Staff
from prettytable import PrettyTable

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
        # Assign person living_space
        if wants_accomodation == "Y" and person_type.lower() == "fellow":
            accomodation_rooms = [room for room in self.all_rooms if room.room_type == "living_space"]
            for living_room in accomodation_rooms:
                if not living_room.fully_occupied:
                    living_room.add_person_to_room(person)
                    person.has_living_space = True
                    rooms.append({"living_space": living_room.room_name})
                    print("{0} has been allocated the living space {1}".format(first_name, office.room_name))
                    break
            if not person.has_living_space:
                print("Sorry, there are no more free accomodation rooms for {0} to occupy.".format(first_name))
        person.rooms_occupied = rooms
        print({"Person": person.first_name + " " + person.last_name, "Rooms": rooms})
        return {"Person": person.first_name + " " + person.last_name, "Rooms": rooms}

    def print_room(self, room_name):
        output = "\n".join(self.find_room(room_name).get_people_in_room())
        print(self.find_room(room_name).get_people_in_room())
        return self.find_room(room_name).get_people_in_room()

    def print_allocations(self, file_name = "", print_table = "N"):
        if print_table != "Y":
            rooms_people = []
            for room in self.all_rooms:
                # people = ",".join([(person.get_fullname()).upper() for person in room.residents])
                people = [(person.get_fullname()).upper() for person in room.residents]
                rooms_people.append({room.room_name: people})
                output = "Room: {0} \n ------------------------------------- \n{1}\n".format(room.room_name,",".join(people))
                if file_name == "":
                    print(output)
                else:
                    file = open(file_name, "w")
                    file.write(str(output))
                    file.close()
            return rooms_people
        else:
            allocated_people = [person for person in self.all_people if len(person.rooms_occupied) != 0]
            if len(allocated_people) > 0:
                table = PrettyTable(['Name', 'Type', 'Office', 'Living Space'])
                for person in allocated_people:
                    office_name, living_space_name = "Not Assigned", "Not Assigned"
                    for i in range(0, len(person.rooms_occupied)):
                        if "office" in person.rooms_occupied[i]: office_name = person.rooms_occupied[i]['office']
                        if "living_space" in person.rooms_occupied[i]: living_space_name = person.rooms_occupied[i]['living_space']
                    table.add_row([person.get_fullname(), person.person_type, office_name, living_space_name])
            print("List showing people with space and their respective rooms")
            print(table)

    def print_unallocated(self):
        unallocated_people = []
        unallocated_table = PrettyTable(['Name', 'Missing'])
        for person in self.all_people:
            if person.wants_accomodation == "N":
                if not person.has_office:
                    unallocated_people.append({"Name": person.get_fullname(), "Missing": "Office"})
                    unallocated_table.add_row([person.get_fullname(), "Office"])
            else:
                if not person.has_office and not person.has_living_space:
                    unallocated_people.append({"Name": person.get_fullname(), "Missing": "Office and Living Space"})
                    unallocated_table.add_row([person.get_fullname(), "Office and Living Space"])
        print(unallocated_table)

    # TODO Cater for Room not found
    def find_room(self, room_name):
        room =[room for room in self.all_rooms if room_name == room.room_name]
        if len(room) > 0:
            return [room for room in self.all_rooms if room_name == room.room_name][0]

    # TODO Cater for Person not found
    def find_person(self, person_id):
        return [person for person in self.all_people if person_id == person.person_id][0]