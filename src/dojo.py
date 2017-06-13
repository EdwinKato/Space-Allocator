"""class Dojo

This class is responsible for managing rooms and people as well as storing and
restoring application state.

Example:
    To create a new instance from another class, use
        dojo = Dojo()

Attributes:
    all_rooms (Room[]): Contains a list of all rooms in the dojo
    all_people (Person[]) Contains a list of all people in the system
"""

import sqlite3
import random
import colorful
from prettytable import PrettyTable
from .living_space import LivingSpace
from .office import Office
from .fellow import Fellow
from .staff import Staff

class Dojo(object):
    """Dojo
    """

    def __init__(self):
        self.all_rooms = []
        self.all_people = []

    def create_room(self, room_type, *room_names):
        """ Used to create new rooms.

        Args:
            room_type (str): Type of room.
            room_names : List of room_names. It takes in one or more names

        Returns:
            Room || Room[]: One Room if one name is provided
            and a list of Rooms if more than one is provided.

        """

        created_rooms = []

        for room_name in room_names:
            # Check if room_name exists in the already created rooms
            if room_name not in [room.room_name for room in self.all_rooms]:
                # Check that room_name contains only alphabetic characters
                if not room_name.isalpha():
                    print("room name input must be string alphabet type")
                    return
                room = Office(
                    room_name) if room_type == "office" else LivingSpace(room_name)
                self.all_rooms.append(room)
                created_rooms.append(room)
                print(
                    colorful.green(
                        "{0} called {1} has been successfully created!"
                        .format(room_type.capitalize(), room_name)))
            else:
                print(
                    colorful.red(
                        "Room with name: {0} already exists. Please try using another name"
                        .format(room_name)))
                break
        return created_rooms[0] if len(created_rooms) == 1 else created_rooms

    def add_person(
            self, first_name,
            last_name, person_type, wants_accommodation="N"):
        """ Used to create a new Person instance.

        Args:
            first_name (str): First name.
            last_name (str): Last name.
            person_type (str): Type of person ie Fellow / Staff.
            wants_accommodation : Indicates wether someone wants accomodation or not.
            Can be N for No or Y for Yes

        Returns:
            Room !! Room[]: The return value. One Room is one name is provided
            and a list of Rooms if more than one is provided.

        """

        rooms = []

        person_id = len(self.all_people) + 1 # Generate person_id
        if not first_name.isalpha() or not last_name.isalpha():
            print(colorful.orange("Name should only contain alphabetic characters.\
                Please rectify and try again"))
            return
        person = Staff(first_name, last_name, person_id) \
            if person_type.lower() == "staff" else Fellow(
                first_name, last_name, wants_accommodation, person_id)
        print(colorful.green(
            "{0} {1} {2} has been successfully added"
            .format(person_type, first_name, last_name)))
        self.all_people.append(person)
        # Assign office to person
        office_rooms = \
            [room for room in self.all_rooms if room.room_type.lower() == "office"\
            and not room.fully_occupied]
        # chosen_room = random.choice(office_rooms)
        if office_rooms:
            chosen_room = random.choice(office_rooms)
            chosen_room.add_person_to_room(person)
            person.has_office = True
            rooms.append({"office": chosen_room.room_name})
            print(
                colorful.green(
                    "{0} has been allocated the office {1}".format(
                        first_name,
                        chosen_room.room_name)))
        else:
            print(
                colorful.red(
                    "Sorry, there are no more office rooms for {0} to occupy.".format(first_name)))

        # Assign person living_space
        if wants_accommodation == "Y" and person_type.lower() == "fellow":
            accommodation_rooms = [
                room for room in self.all_rooms if room.room_type == "living_space"]
            for living_room in accommodation_rooms:
                if not living_room.fully_occupied:
                    living_room.add_person_to_room(person)
                    person.has_living_space = True
                    rooms.append({"living_space": living_room.room_name})
                    print(
                        colorful.green(
                            "{0} has been allocated the living space {1}".format(
                                first_name,
                                living_room.room_name)))
                    break
            if not person.has_living_space:
                print(
                    colorful.red(
                        "Sorry, there are no more free accommodation rooms for {0} to occupy."
                        .format(first_name)))
        person.rooms_occupied = rooms
        return {"Person": person.first_name + " " + person.last_name, "Rooms": rooms}

    def print_room(self, room_name):
        """Prints all the people in a room """

        if room_name in [room.room_name for room in self.all_rooms]:
            output = "\n".join(self.find_room(room_name).get_people_in_room())
            print(
                colorful.blue(
                    "People in Room: " + room_name +
                    "\n --------------------------------------------------------------------"))
            print(
                colorful.blue(
                    ", ".join(
                        self.find_room(room_name).get_people_in_room())))
            return self.find_room(room_name).get_people_in_room()
        else:
            print(
                colorful.red(
                    room_name +
                    " does not exist in the system. Please change name and try again!"))
            return []

    def print_allocations(self, file_name="", print_table="N"):
        """Prints the people and respective rooms"""

        if print_table != "Y":
            rooms_people = []
            printed_output = ""
            for room in self.all_rooms:
                people = [(person.get_fullname()).upper()
                          for person in room.residents]
                rooms_people.append({room.room_name: people})
                output = "Room: {0} \n ------------------------------------- \n{1}\n\n".format(
                    room.room_name, ",".join(people))
                printed_output += output
            if not file_name:
                if printed_output:
                    print(colorful.blue(printed_output))
                else:
                    print(colorful.orange("There are no people allocated to any rooms at the moment"))
            else:
                file = open(file_name, "w")
                file.write(str(printed_output))
                file.close()
            return rooms_people
        else:
            allocated_people = \
                [person for person in self.all_people if person.rooms_occupied]
            if allocated_people:
                table = PrettyTable(['Name', 'Type', 'Office', 'Living Space'])
                for person in allocated_people:
                    office_name, living_space_name = "Not Assigned", "Not Assigned"
                    for i in range(0, len(person.rooms_occupied)):
                        if "office" in person.rooms_occupied[i]:
                            office_name = person.rooms_occupied[i]['office']
                        if "living_space" in person.rooms_occupied[i]:
                            living_space_name = person.rooms_occupied[i]['living_space']
                    table.add_row(
                        [person.get_fullname(), person.person_type, office_name, living_space_name])
                print(
                    colorful.blue("List showing people with space and their respective rooms"))
                print(colorful.blue(table))
            else:
                print(colorful.orange("There are no people allocated to any rooms at the moment"))

    def print_unallocated(self):
        """Prints unallocated people along with the missing room type"""

        unallocated_people = []
        unallocated_table = PrettyTable(['Name', 'Person id', 'Missing'])
        for person in self.all_people:
            if person.wants_accommodation == "N":
                if not person.has_office:
                    unallocated_people.append(
                        {"Name": person.get_fullname(), "Missing": "Office"})
                    unallocated_table.add_row(
                        [person.get_fullname(), person.person_id, "Office"])
            else:
                if not person.has_office and not person.has_living_space:
                    unallocated_people.append(
                        {"Name": person.get_fullname(), "Missing": "Office and Living Space"})
                    unallocated_table.add_row(
                        [person.get_fullname(), person.person_id, "Office and Living Space"])
                elif not person.has_office and person.has_living_space:
                    unallocated_people.append(
                        {"Name": person.get_fullname(), "Missing": "Office"})
                    unallocated_table.add_row(
                        [person.get_fullname(), person.person_id, "Office"])
                elif person.has_office and not person.has_living_space:
                    unallocated_people.append(
                        {"Name": person.get_fullname(), "Missing": "Living Space"})
                    unallocated_table.add_row(
                        [person.get_fullname(), person.person_id, "Living Space"])
        print(colorful.blue("Table showing people along with missing rooms"))
        print(colorful.blue(unallocated_table))

    def find_room(self, room_name):
        """Takes in the room name and returns the room"""

        return [room for room in self.all_rooms if room_name == room.room_name][0]

    def find_person(self, person_id):
        """Takes in the person_id and returns the person"""

        return [person for person in self.all_people if person_id ==
                person.person_id][0]

    def load_people(self, file):
        """Loads the people from the text file to the system"""

        file = open(file, "r")
        for line in file:
            person_data = line.split()
            if len(person_data) == 4:
                self.add_person(
                    person_data[0],
                    person_data[1],
                    person_data[2],
                    person_data[3])
            else:
                self.add_person(person_data[0], person_data[1], person_data[2])
        file.close()

    def reallocate_person(self, person_id, new_room_name):
        """Reallocates person from one room to another"""

        if person_id in [person.person_id for person in self.all_people]:
            person = self.find_person(person_id)
            new_room = self.find_room(new_room_name)
            if not new_room.fully_occupied:
                if new_room.room_type == "office":
                    old_office = [elem['office']
                                  for elem in person.rooms_occupied if 'office' in elem]
                    if not old_office:
                        new_room.add_person_to_room(person)
                        person.rooms_occupied.append({'office': new_room_name})
                        person.has_office = True
                        print(colorful.green(
                            person.get_fullname().capitalize() +
                            " has been assigned to room " +
                            new_room.room_name))
                    else:
                        current_room = self.find_room(old_office[0])
                        if current_room.room_name == new_room_name:
                            print(colorful.red(
                                "Can not reallocate to the same room. \
                                Please specify another room name and try again!"))
                            return
                        if new_room.room_type != current_room.room_type:
                            print(colorful.red(
                                "Can not reallocate to different room type. \
                                Please specify another type and try again!"))
                            return
                        current_room.remove_person_from_room(person)
                        new_room.add_person_to_room(person)
                        for elem in person.rooms_occupied:
                            if 'office' in elem:
                                elem['office'] = new_room_name
                        print(
                            colorful.green(
                                "{0} {1} has been successfully reallocated to room {2}".format(
                                    person.first_name,
                                    person.last_name,
                                    new_room_name)))
                else:
                    old_living_space = [
                        elem['living_space'] \
                        for elem in person.rooms_occupied if 'living_space' in elem]
                    if not old_living_space:
                        new_room.add_person_to_room(person)
                        person.rooms_occupied.append(
                            {'living_space': new_room_name})
                        person.has_living_space = True
                        print(
                            colorful.green(
                                person.get_fullname().capitalize() +
                                " has been assigned to room " +
                                new_room.room_name))
                    else:
                        current_room = self.find_room(old_living_space[0])
                        # current_room = self.find_room(
                            # person.rooms_occupied[i]['living_space'])
                        if current_room.room_name == new_room_name:
                            print(colorful.red(
                                "Can not reallocate to the same room. \
                                Please specify room name and try again."))
                            return
                        if new_room.room_type != current_room.room_type:
                            print(colorful.red(
                                "Can not reallocate to different room type. \
                                Please specify another type and try again."))
                            return
                        current_room.remove_person_from_room(person)
                        new_room.add_person_to_room(person)
                        for elem in person.rooms_occupied:
                            if 'living_space' in elem:
                                elem['living_space'] = new_room_name
                        print(
                            colorful.green(
                                "{0} {1} has been successfully reallocated to room {2}".format(
                                    person.first_name,
                                    person.last_name,
                                    new_room_name)))
            else:
                print(
                    colorful.red(
                        "Room: " +
                        new_room.room_name +
                        "is fully occupied. Please change room and try again"))
        else:
            print(
                colorful.red(
                    "Person with person id " +
                    person_id +
                    " does not exist in the system. Please change id and try again"))

    def save_state(self, db_file=""):
        """Saves all the data in the system to a file specified"""

        connection = sqlite3.connect(
            ":memory:") if db_file == "" else sqlite3.connect(db_file)
        cursor = connection.cursor()

        # Create Room table
        cursor.execute('''CREATE TABLE IF NOT EXISTS room
                     (room_name text, room_type text, occupation_status text)''')

        # Save room data
        room_data = []
        for room in self.all_rooms:
            room_data.append(
                (room.room_name, room.room_type, room.fully_occupied))
        cursor.executemany("INSERT INTO room VALUES (?,?,?)", room_data)

        # Create Person table
        cursor.execute('''CREATE TABLE IF NOT EXISTS person
                     (person_id INTEGER, first_name text, last_name text, person_type text,
                     has_living_space text, has_office text,wants_accommodation text
                     )''')

        # Save person data
        person_data = []
        for person in self.all_people:
            person_data.append(
                (person.person_id,
                 person.first_name,
                 person.last_name,
                 person.person_type,
                 person.has_living_space,
                 person.has_office,
                 person.wants_accommodation))
        cursor.executemany(
            "INSERT INTO person VALUES (?,?,?,?,?,?,?)",
            person_data)

        # Create room_person relationship table table
        cursor.execute('''CREATE TABLE IF NOT EXISTS room_person
                     (person_id INTEGER, room_name text, room_type text)''')

        # Save room_person data
        room_person_data = []
        for person in self.all_people:
            for i in range(0, len(person.rooms_occupied)):
                if "office" in person.rooms_occupied[i]:
                    room_person_data.append(
                        (person.person_id, person.rooms_occupied[i]['office'], "office"))
                if "living_space" in person.rooms_occupied[i]:
                    room_person_data.append(
                        (person.person_id, person.rooms_occupied[i]['living_space'], "living_space"))

        cursor.executemany(
            "INSERT INTO room_person VALUES (?,?,?)",
            room_person_data)

        # Save (commit) the changes
        connection.commit()
        connection.close()

    def load_state(self, db_file=""):
        """Loads application data from a db file to the application"""

        connection = sqlite3.connect(
            ":memory:") if db_file == "" else sqlite3.connect(db_file)
        cursor = connection.cursor()

        try:
            # Load Rooms
            cursor.execute('''SELECT * FROM room''')
            rooms = cursor.fetchall()
            for room in rooms:
                room_name, room_type, occupation_status = room[0], room[1], room[2]
                loaded_room = self.create_room(room_type, room_name)
        except BaseException:
            print(colorful.red(
                "The application has failed to load room data, \
                please contact a senior developer for help."))

        try:
            # Load People
            cursor.execute('''SELECT * FROM person''')
            people = cursor.fetchall()
            for person in people:
                person_id, first_name, last_name, person_type, has_living_space, \
                 has_office, wants_accommodation \
                    = person[0], person[1], person[2], person[3], person[4], person[5], person[6]

                loaded_person = Staff(
                    first_name,
                    last_name,
                    person_id,
                    has_living_space,
                    has_office) if person_type == "Staff" else Fellow(
                        first_name,
                        last_name,
                        wants_accommodation,
                        person_id,
                        has_living_space,
                        has_office)
                self.all_people.append(loaded_person)
        except BaseException:
            print(colorful.red(
                "The application has failed to load person data, \
                please contact a senior developer for help."))

        try:
            # Load Residents
            cursor.execute('''SELECT * FROM room_person''')
            room_person_data = cursor.fetchall()
            for room_person in room_person_data:
                person_id, room_name, room_type = int(
                    room_person[0]), room_person[1], room_person[2]
                related_room = self.find_room(room_name)
                related_person = self.find_person(person_id)
                related_room.residents.append(related_person)
                related_person.rooms_occupied.append({room_type: room_name})
        except BaseException:
            print(colorful.red(
                "The application has failed to load relationship between person and room, \
                Please contact a senior developer for help."))
