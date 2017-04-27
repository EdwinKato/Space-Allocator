from .person import Person


class Fellow(Person):

    def __init__(self, first_name, last_name, wants_accommodation, person_id, has_living_space = None, has_office = None):
        super(Fellow, self).__init__(first_name, last_name, "fellow", wants_accommodation, person_id, has_living_space, has_office)

