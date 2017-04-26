from .person import Person


class Staff(Person):

    def __init__(self, first_name, last_name, person_type, person_id, has_living_space = None, has_office = None):
        super(Staff, self).__init__(first_name, last_name, person_type, "N", person_id, has_living_space, has_office)

