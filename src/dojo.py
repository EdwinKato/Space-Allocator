"""class Dojo

This class is responsible for managing rooms and people as well as storing and
restoring application state.

Example:
    To create a new instance from another class, use
        dojo = Dojo()

Attributes:
    rooms (Room[]): Contains a list of all rooms in the dojo
    people (Person[]) Contains a list of all people in the system
"""

import random
import sqlite3
import os.path

import colorful
from prettytable import PrettyTable

from .living_space import LivingSpace
from .office import Office
from .fellow import Fellow
from .staff import Staff
from .helpers import get_residents, remove_person, \
    find_room, find_person, add_person_to_room


class Dojo(object):
    """Dojo
    """

    def __init__(self):
        self.rooms = []
        self.people = []

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
            if room_name not in [room.name for room in self.rooms]:
                # Check that room_name contains only alphabetic characters
                if not room_name.isalpha():
                    print("room name input must be string alphabet type")
                    return
                room = Office(room_name) if room_type.lower(
                ) == "office" else LivingSpace(room_name)
                self.rooms.append(room)
                created_rooms.append(room)
                print(
                    colorful.green(
                        "{0} called {1} has been successfully created!"
                        .format(room_type.capitalize(), room_name)))
            else:
                print(
                    colorful.red(
                        "Room with name: {0} already exists. "
                        "Please try using another name"
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
            wants_accommodation : Indicates wether someone wants accomodation.
            Can be N for No or Y for Yes

        Returns:
            Room !! Room[]: The return value. One Room is one name is provided
            and a list of Rooms if more than one is provided.

        """

        rooms = []

        person_id = len(self.people) + 1  # Generate person_id
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
        self.people.append(person)
        # Assign office to person
        office_rooms = \
            [room for room in self.rooms if room._type.lower() == "office"
                and not room.fully_occupied]
        # chosen_room = random.choice(office_rooms)
        if office_rooms:
            chosen_room = random.choice(office_rooms)
            add_person_to_room(person, chosen_room)
            person.has_office = True
            rooms.append({"office": chosen_room.name})
            print(
                colorful.green(
                    "{0} has been allocated the office {1}".format(
                        first_name,
                        chosen_room.name)))
        else:
            print(
                colorful.red(
                    "Sorry, No more office rooms for {0} to occupy."
                    .format(first_name)))

        if wants_accommodation is "Y" and person_type.lower() == "staff":
            print(colorful.red(
                "Sorry, No living space has been allocated to you as these"
                " are only meant for fellows."))

        # Assign person living_space
        if wants_accommodation is "Y" and person_type.lower() == "fellow":
            accommodation_rooms = [
                room for room in self.rooms if room._type is "living_space"]
            for living_room in accommodation_rooms:
                if not living_room.fully_occupied:
                    add_person_to_room(person, living_room)
                    person.has_living_space = True
                    rooms.append({"living_space": living_room.name})
                    print(
                        colorful.green(
                            "{0} has been allocated the living space {1}"
                            .format(
                                first_name,
                                living_room.name)))
                    break
            if not person.has_living_space:
                print(
                    colorful.red(
                        "Sorry, there are no more free accommodation rooms"
                        "for {0} to occupy."
                        .format(first_name)))
        person.rooms_occupied = rooms
        return {
            "Person": person.first_name +
            " " +
            person.last_name,
            "Rooms": rooms}

    def print_room(self, room_name):
        """Prints all the people in a room """

        if room_name in [room.name for room in self.rooms]:
            # output = "\n".join(get_residents
            # (find_room(self.rooms, room_name)))
            print(
                colorful.blue(
                    "People in Room: " +
                    room_name +
                    "\n -----------------------------------"
                    "---------------------------------"))
            print(
                colorful.blue(
                    ", ".join(
                        get_residents(find_room(self.rooms, room_name)))))
            return get_residents(find_room(self.rooms, room_name))
        else:
            print(
                colorful.red(
                    room_name +
                    " does not exist in the system."
                    "Please change name and try again!"))
            return []

    def print_allocations(self, file_name=None, print_table="N"):
        """Prints the people and respective rooms"""

        if print_table is "N":
            rooms_people = []
            printed_output = ""
            for room in self.rooms:
                people = [(person.get_fullname()).upper()
                          for person in room.residents]
                rooms_people.append({room.name: people})
                output = "Room: {0} \n ------\n{1}\n\n".format(
                    room.name, ",".join(people))
                printed_output += output
            if not file_name:
                if printed_output:
                    print(colorful.blue(printed_output))
                else:
                    print(
                        colorful.orange("There are "
                                        "no people allocated to "
                                        "any rooms at the moment"))
            else:
                file = open("resources/" + file_name, "w")
                file.write(str(printed_output))
                file.close()
            return rooms_people
        else:
            allocated_people = \
                [person for person in self.people if person.rooms_occupied]
            if allocated_people:
                table = PrettyTable(['Name', 'Type', 'Office', 'Living Space'])
                for person in allocated_people:
                    office_name, living_space_name \
                     = "Not Assigned", "Not Assigned"
                    for room_occupied in range(0, len(person.rooms_occupied)):
                        if "office" in person.rooms_occupied[room_occupied]:
                            office_name = \
                                person.rooms_occupied[room_occupied]['office']
                        if "living_space" in\
                                person.rooms_occupied[room_occupied]:
                            living_space_name \
                                = person.rooms_occupied[room_occupied]['living_space']
                    table.add_row(
                        [person.get_fullname(),
                         person._type, office_name, living_space_name])
                print(
                    colorful.blue(
                        "List showing people with space "
                        "and their respective rooms"))
                print(colorful.blue(table))
            else:
                print(
                    colorful.orange("There are no people allocated"
                                    " to any rooms at the moment"))

    def print_unallocated(self):
        """Prints unallocated people along with the missing room type"""

        unallocated_people = []
        unallocated_table = PrettyTable(['Name', 'Person id', 'Missing'])
        for person in self.people:
            if person.wants_accommodation is "N":
                if not person.has_office:
                    unallocated_people.append(
                        {"Name": person.get_fullname(), "Missing": "Office"})
                    unallocated_table.add_row(
                        [person.get_fullname(), person.id_, "Office"])
            else:
                if not person.has_office and not person.has_living_space:
                    unallocated_people.append(
                        {"Name": person.get_fullname(),
                         "Missing": "Office and Living Space"})
                    unallocated_table.add_row(
                        [person.get_fullname(), person.id_,
                         "Office and Living Space"])
                elif not person.has_office and person.has_living_space:
                    unallocated_people.append(
                        {"Name": person.get_fullname(), "Missing": "Office"})
                    unallocated_table.add_row(
                        [person.get_fullname(), person.id_, "Office"])
                elif person.has_office and not person.has_living_space:
                    unallocated_people.append(
                        {"Name": person.get_fullname(),
                         "Missing": "Living Space"})
                    unallocated_table.add_row(
                        [person.get_fullname(), person.id_, "Living Space"])
        print(colorful.blue("Table showing people along with missing rooms"))
        print(colorful.blue(unallocated_table))

    def load_people(self, file):
        """Loads the people from the text file to the system"""

        if os.path.isfile(file):
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
                    self.add_person(
                        person_data[0], person_data[1], person_data[2])
            file.close()
        else:
            print(colorful.red("File does not exist! "
                               "Please specify another file"))

    def reallocate_person(self, person_id, new_room_name):
        """Reallocates person from one room to another"""

        if person_id in [person.id_ for person in self.people]:
            person = find_person(self.people, person_id)
            new_room = find_room(self.rooms, new_room_name)
            if not new_room.fully_occupied:
                if new_room._type is "office":
                    old_office = [elem['office']
                                  for elem in person.rooms_occupied
                                  if 'office' in elem]
                    if not old_office:
                        add_person_to_room(person, new_room)
                        person.rooms_occupied.append({'office': new_room_name})
                        person.has_office = True
                        print(colorful.green(
                            person.get_fullname().capitalize() +
                            " has been assigned to room " +
                            new_room.name))
                    else:
                        current_room = find_room(self.rooms, old_office[0])
                        if current_room.name == new_room_name:
                            print(colorful.red(
                                "Can not reallocate to the same room. "
                                "Please specify another room name and "
                                "try again!"))
                            return
                        if new_room._type != current_room._type:
                            print(colorful.red(
                                "Can not reallocate to different room type. \
                                Please specify another type and try again!"))
                            return
                        remove_person(person, current_room)
                        add_person_to_room(person, new_room)
                        for elem in person.rooms_occupied:
                            if 'office' in elem:
                                elem['office'] = new_room_name
                        print(
                            colorful.green(
                                "{0} {1} has been successfully reallocated "
                                "to room {2}".format(
                                    person.first_name,
                                    person.last_name,
                                    new_room_name)))
                else:
                    old_living_space = [
                        elem['living_space']
                        for elem in person.rooms_occupied
                        if 'living_space' in elem]
                    if not old_living_space:
                        add_person_to_room(person, new_room)
                        person.rooms_occupied.append(
                            {'living_space': new_room_name})
                        person.has_living_space = True
                        print(
                            colorful.green(
                                person.get_fullname().capitalize() +
                                " has been assigned to room " +
                                new_room.name))
                    else:
                        current_room = find_room(
                            self.rooms, old_living_space[0])
                        if current_room.name == new_room_name:
                            print(colorful.red(
                                "Can not reallocate to the same room. \
                                Please specify room name and try again."))
                            return
                        if new_room._type != current_room._type:
                            print(colorful.red(
                                "Can not reallocate to different room type. \
                                Please specify another type and try again."))
                            return
                        remove_person(person, current_room)
                        add_person_to_room(person, new_room)
                        for elem in person.rooms_occupied:
                            if 'living_space' in elem:
                                elem['living_space'] = new_room_name
                        print(
                            colorful.green(
                                "{0} {1} has been successfully reallocated"
                                " to room {2}".format(
                                    person.first_name,
                                    person.last_name,
                                    new_room_name)))
            else:
                print(
                    colorful.red(
                        "Room: " +
                        new_room.name +
                        "is fully occupied. Please change room and try again"))
        else:
            print(
                colorful.red(
                    "Person with person id " +
                    person_id +
                    " does not exist in the system."
                    "Please change id and try again"))

    def save_state(self, db_file=None):
        """Saves all the data in the system to a file specified"""

        connection = sqlite3.connect(
            ":memory:") \
            if not db_file else sqlite3.connect("resources/" + db_file)
        cursor = connection.cursor()

        # Create Room table
        cursor.execute('''CREATE TABLE IF NOT EXISTS room
                     (room_name text, room_type text,
                      occupation_status text)''')

        # Save room data
        room_data = []
        for room in self.rooms:
            room_data.append(
                (room.name, room._type, room.fully_occupied))
        cursor.executemany("INSERT INTO room VALUES (?,?,?)", room_data)

        # Create Person table
        cursor.execute('''CREATE TABLE IF NOT EXISTS person
                     (person_id INTEGER, first_name text,
                     last_name text, person_type text,
                     has_living_space text, has_office text,
                     wants_accommodation text
                     )''')

        # Save person data
        person_data = []
        for person in self.people:
            person_data.append(
                (person.id_,
                 person.first_name,
                 person.last_name,
                 person._type,
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
        for person in self.people:
            for room_occupied in range(0, len(person.rooms_occupied)):
                if "office" in person.rooms_occupied[room_occupied]:
                    room_person_data.append(
                        (person.id_,
                         person.rooms_occupied[room_occupied]['office'],
                         "office"))
                if "living_space" in person.rooms_occupied[room_occupied]:
                    room_person_data.append(
                        (person.id_,
                         person.rooms_occupied[room_occupied]['living_space'],
                         "living_space"))

        cursor.executemany(
            "INSERT INTO room_person VALUES (?,?,?)",
            room_person_data)

        # Save (commit) the changes
        connection.commit()
        connection.close()

    def load_state(self, db_file=None):
        """Loads application data from a db file to the application"""

        connection = sqlite3.connect(
            ":memory:") if not db_file else sqlite3.connect(db_file)
        cursor = connection.cursor()

        try:
            # Load Rooms
            cursor.execute('''SELECT * FROM room''')
            rooms = cursor.fetchall()
            for room in rooms:
                room_name, room_type = room[0], room[1]
                self.create_room(room_type, room_name)
        except BaseException:
            print(colorful.red(
                "The application has failed to load room data, \
                please contact a senior developer for help."))

        try:
            # Load People
            cursor.execute('''SELECT * FROM person''')
            people = cursor.fetchall()
            for person in people:
                person_id, first_name, last_name, person_type,\
                    has_living_space, \
                    has_office, wants_accommodation \
                    = person[0], person[1], person[2], person[3],\
                    person[4], person[5], person[6]

                loaded_person = Staff(
                    first_name,
                    last_name,
                    person_id,
                    has_living_space,
                    has_office) if person_type is "Staff" else Fellow(
                        first_name,
                        last_name,
                        wants_accommodation,
                        person_id,
                        has_living_space,
                        has_office)
                self.people.append(loaded_person)
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
                related_room = find_room(self.rooms, room_name)
                related_person = find_person(self.people, person_id)
                related_room.residents.append(related_person)
                related_person.rooms_occupied.append({room_type: room_name})
        except BaseException:
            print(colorful.red(
                "The application has failed to load relationship between person and room, \
                Please contact a senior developer for help."))
