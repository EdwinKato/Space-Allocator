"""Room

This class is responsible for managing people in a room.
Example:
    To create a new instance, use
        room = Room()

Attributes:
    residents (Person[]): People currently leaving in the room
    room_name (str): Name of room.
    room_type (str): Type of room ie Office / LivingSpace
    fully_occupied : True indicates that the room is occupied to capacity
"""

class Room(object):
    """ This class is responsible for managing the people in a room """

    def __init__(self, room_type, room_name):
        self.residents = []
        self.room_name = room_name
        self.room_type = room_type
        self.fully_occupied = None

        if room_type == "office":
            self.maximum_no_of_people = 6
        else:
            self.maximum_no_of_people = 4

    def add_person_to_room(self, person):
        """ Add person to room

        Args:
            person (Person): Person to be added to room

        """

        if len(self.residents) != self.maximum_no_of_people:
            self.residents.append(person)
            if len(self.residents) == self.maximum_no_of_people:
                self.fully_occupied = True
            return True
        else:
            return False

    def get_people_in_room(self):
        """ Get people in room

        Returns:
            Array of names of the people in the room

        """

        people = []
        for person in self.residents:
            people.append(person.get_fullname())
        return people

    def remove_person_from_room(self, person):
        """Removes a person from a room

        Args:
            person (Person): Person to be removed from the room

        Returns:
            True if successful, False otherwise.
        """

        if person in self.residents:
            self.residents.remove(person)
            if self.fully_occupied:
                self.fully_occupied = None
            return True
        else:
            return False
