def get_residents(room):
    """Get people in room

    Returns:
        Array of names of the people in the room

    """

    people = []
    for person in room.residents:
        people.append(person.get_fullname())
    return people


def remove_person(person, room):
    """Removes a person from a room

    Args:
        person (Person): Person to be removed from the room

    Returns:
        True if successful, False otherwise.
    """

    if person in room.residents:
        room.residents.remove(person)
        if room.fully_occupied:
            room.fully_occupied = None
        return True
    else:
        return False


def find_room(rooms, room_name):
    """Takes in the room name and returns the room"""

    return [room for room in rooms if room_name == room.name][0]


def find_person(people, person_id):
    """Takes in the person_id and returns the person"""

    return [person for person in people if person_id == person.id_][0]


def add_person_to_room(person, room):
    """ Add person to room

    Args:
        person (Person): Person to be added to room
        room (Room): Room to which person is to be added

    """

    if len(room.residents) < room.maximum_no_of_people:
        room.residents.append(person)
        if len(room.residents) == room.maximum_no_of_people:
            room.fully_occupied = True
        return True
    else:
        return False
