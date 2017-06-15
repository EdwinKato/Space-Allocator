"""Class definition of Staff

"""

from .person import Person


class Staff(Person):
    """Staff

    """

    def __init__(self, first_name, last_name, person_id, \
        has_living_space=None, has_office=None):
        super(Staff, self).__init__(first_name, last_name, \
            "N", person_id, has_living_space, has_office)
        self.set_type()

    def set_type(self):
        self._type = "staff"
