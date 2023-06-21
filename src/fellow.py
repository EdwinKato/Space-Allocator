"""Class definition of Fellow

It inherits directly from Person

"""

from .person import Person


class Fellow(Person):
    """Fellow

    """

    def __init__(self, first_name, last_name, wants_accommodation,
                 person_id, has_living_space=None, has_office=None):
        super(
            Fellow,
            self).__init__(
            first_name,
            last_name,
            wants_accommodation,
            person_id,
            has_living_space,
            has_office)
        self.set_type()

    def set_type(self):
        self._type = "fellow"
