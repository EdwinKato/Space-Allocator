from .living_space import LivingSpace
from .office import Office
from .fellow import Fellow
from .staff import Staff
from prettytable import PrettyTable
import sqlite3

class Dojo(object):
    """This class is responsible for managing and allocating rooms to people"""

    def __init__(self):
        self.all_rooms = []
        self.all_people = []

    def create_room(self, room_type, *room_names):
        created_rooms = []
        for room_name in room_names:
            if room_name not in [room.room_name for room in self.all_rooms]:
                room = Office(room_name) if room_type == "office" else LivingSpace(room_name)
                self.all_rooms.append(room)
                created_rooms.append(room)
                print("An {0} called {1} has been successfully created!".format(room_type, room_name))
            else:
                print("Room with name: {0} already exists. Please try using another name".format(room_name))
        return created_rooms[0] if len(created_rooms) == 1 else created_rooms

    def add_person(self, first_name, last_name, person_type, wants_accommodation = "N"):
        rooms = []
        person_id = len(self.all_people) + 1
        person = Staff(first_name, last_name, person_id) if person_type.lower() == "staff" else\
            Fellow(first_name, last_name, wants_accommodation, person_id)
        print("{0} {1} {2} has been successfully added".format(person_type, first_name, last_name))
        self.all_people.append(person)
        # Assign office to person
        office_rooms = [room for room in self.all_rooms if room.room_type.lower() == "office"]
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
        if wants_accommodation == "Y" and person_type.lower() == "fellow":
            accommodation_rooms = [room for room in self.all_rooms if room.room_type == "living_space"]
            for living_room in accommodation_rooms:
                if not living_room.fully_occupied:
                    living_room.add_person_to_room(person)
                    person.has_living_space = True
                    rooms.append({"living_space": living_room.room_name})
                    print("{0} has been allocated the living space {1}".format(first_name, office.room_name))
                    break
            if not person.has_living_space:
                print("Sorry, there are no more free accommodation rooms for {0} to occupy.".format(first_name))
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
            if person.wants_accommodation == "N":
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

    def load_people(self, file):
        file = open(file, "r")
        for line in file:
            person_data = line.split()
            if len(person_data) == 4:
                self.add_person(person_data[0], person_data[1], person_data[2], person_data[3])
            else:
                self.add_person(person_data[0], person_data[1], person_data[2])
        file.close()

    def reallocate_person(self, person_id, new_room_name):
        person = self.find_person(person_id)
        new_room = self.find_room(new_room_name)
        if not new_room.fully_occupied:
            for i in range(0, len(person.rooms_occupied)):
                if new_room.room_type == "office":
                    if "office" in person.rooms_occupied[i]:
                        current_room = self.find_room(person.rooms_occupied[i]['office'])
                        if current_room.room_name == new_room_name:
                            print(
                                "Can not reallocate to the same room. Please specify room name and try again.")
                            return
                        if new_room.room_type != current_room.room_type:
                            print("Can not reallocate to different room type. Please specify another type and try again.")
                            return
                        current_room.remove_person_from_room(person)
                        new_room.add_person_to_room(person)
                        person.rooms_occupied[i]['office'] = new_room_name
                        print("{0} {1} has been successfully reallocated to room {2}".format(person.first_name,person.last_name, new_room_name))
                else:
                    if "living_space" in person.rooms_occupied[i]:
                        current_room = self.find_room(person.rooms_occupied[i]['living_space'])
                        if current_room.room_name == new_room_name:
                            print(
                                "Can not reallocate to the same room. Please specify room name and try again.")
                            return
                        if new_room.room_type != current_room.room_type:
                            print("Can not reallocate to different room type. Please specify another type and try again.")
                            return
                        current_room.remove_person_from_room(person)
                        new_room.add_person_to_room(person)
                        person.rooms_occupied[i]['living_space'] = new_room_name
                        print("{0} {1} has been successfully reallocated to room {2}".format(person.first_name, person.last_name,new_room_name))

    def save_state(self, db_file = ""):
        connection = sqlite3.connect(":memory:") if db_file == "" else sqlite3.connect(db_file)
        cursor = connection.cursor()

        # Create Room table
        cursor.execute('''CREATE TABLE IF NOT EXISTS room
                     (room_name text, room_type text, occupation_status text)''')

        # Save room data
        room_data = []
        for room in self.all_rooms:
            room_data.append((room.room_name, room.room_type, room.fully_occupied))
        cursor.executemany("INSERT INTO room VALUES (?,?,?)", room_data)

        # Create Person table
        cursor.execute('''CREATE TABLE IF NOT EXISTS person
                     (person_id INTEGER, first_name text, last_name text, person_type text,
                     has_living_space text, has_office text,wants_accommodation text
                     )''')

        # Save person data
        person_data = []
        for person in self.all_people:
            person_data.append((person.person_id, person.first_name, person.last_name, \
                                person.person_type, person.has_living_space,person.has_office,
                                person.wants_accommodation))
        cursor.executemany("INSERT INTO person VALUES (?,?,?,?,?,?,?)", person_data)

        # Create room_person relationship table table
        cursor.execute('''CREATE TABLE IF NOT EXISTS room_person
                     (person_id INTEGER, room_name text, room_type text)''')

        # Save room_person data
        room_person_data = []
        for person in self.all_people:
            for i in range(0, len(person.rooms_occupied)):
                if "office" in person.rooms_occupied[i]:
                    room_person_data.append((person.person_id, person.rooms_occupied[i]['office'], "office"))
                if "living_space" in person.rooms_occupied[i]:
                    room_person_data.append((person.person_id, person.rooms_occupied[i]['living_space'], "living_space"))

        cursor.executemany("INSERT INTO room_person VALUES (?,?,?)", room_person_data)

        # Save (commit) the changes
        connection.commit()
        connection.close()

    def load_state(self, db_file = ""):
        connection = sqlite3.connect(":memory:") if db_file == "" else sqlite3.connect(db_file)
        cursor = connection.cursor()

        # Load Rooms
        cursor.execute('''SELECT * FROM room''')
        rooms = cursor.fetchall()
        for room in rooms:
            room_name, room_type, occupation_status = room[0], room[1], room[2]
            loaded_room = self.create_room(room_type, room_name)

        # Load People
        cursor.execute('''SELECT * FROM person''')
        people = cursor.fetchall()
        for person in people:
            person_id, first_name, last_name, person_type, has_living_space, has_office, wants_accommodation \
                = person[0], person[1], person[2], person[3], person[4], person[5], person[6]

            loaded_person = Staff(first_name, last_name, person_id, has_living_space, has_office)\
                if person_type == "Staff" else Fellow(first_name, last_name, wants_accommodation, person_id,\
                      has_living_space, has_office)
            self.all_people.append(loaded_person)

        # Load Residents
        cursor.execute('''SELECT * FROM room_person''')
        room_person_data = cursor.fetchall()
        for room_person in room_person_data:
            person_id, room_name, room_type = int(room_person[0]), room_person[1], room_person[2]
            related_room = self.find_room(room_name)
            related_person = self.find_person(person_id)
            related_room.residents.append(related_person)
            related_person.rooms_occupied.append({room_type :room_name})
