class Person(object):
    """ This class is responsible for managing people's data """

    # has_living_space, has_office,
    def __init__(self, first_name, last_name, person_type, wants_accomodation, person_id , has_living_space = None, has_office = None):
        self.first_name = first_name
        self.last_name = last_name
        self.person_id = person_id
        self.person_type = person_type
        self.has_living_space = None if has_living_space is None else True
        self.has_office = None if has_office is None else True
        self.rooms_occupied = []
        self.wants_accomodation = wants_accomodation


