"""Class definition of class Person"""

class Person(object):
    """ This class is responsible for managing people's data """

    def __init__(self, first_name, last_name, person_type,\
        wants_accommodation, person_id, has_living_space=None, has_office=None):
        self.first_name = first_name
        self.last_name = last_name
        self.person_id = person_id
        self.person_type = person_type
        self.has_living_space = None if has_living_space is None else True
        self.has_office = None if has_office is None else True
        self.rooms_occupied = []
        self.wants_accommodation = wants_accommodation

    def get_fullname(self):
        """get_fullname()

        Returns:
            Fullname of person
        """

        return self.first_name + " " + self.last_name
