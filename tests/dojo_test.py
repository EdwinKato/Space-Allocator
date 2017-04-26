import unittest
from src.dojo import Dojo


class TestCreateRoom (unittest.TestCase):
    def test_create_room_successfully(self):
        my_class_instance = Dojo()
        initial_room_count = len(my_class_instance.all_rooms)
        blue_office = my_class_instance.create_room("office", "Blue")
        self.assertTrue(blue_office)
        new_room_count = len(my_class_instance.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 1)

    def test_create_rooms_successfully(self):
        my_class_instance = Dojo()
        initial_room_count = len(my_class_instance.all_rooms)
        offices = my_class_instance.create_room("office", "Blue", "Black", "Brown")
        self.assertTrue(offices)
        new_room_count = len(my_class_instance.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 3)

    def test_person_added_to_system(self):
        initial_person_count = len(self.dojo.all_people)
        person = self.dojo.add_person("Neil", "Armstrong", "Staff")
        self.assertTrue(person)
        new_person_count = len(self.dojo.all_people)
        self.assertEqual(new_person_count - initial_person_count, 1)

    def test_person_has_been_assigned_office(self):
        person = self.dojo.add_person("Neil", "Armstrong", "Staff")
        self.assertTrue(person)
        self.assertTrue(self.dojo.all_people[-1].has_office)

    def test_person_has_been_assigned_living_space(self):
        person = self.dojo.add_person("Eden", "Hazard", "Fellow", "Y")
        self.assertTrue(person)
        self.assertTrue(self.dojo.all_people[-1].has_living_space)

    def test_return_type_of_add_person(self):
        person = self.dojo.add_person("Eden", "Hazard", "Fellow", "Y")
        self.assertEqual({'Person': 'Eden Hazard', 'Rooms': [{'office': 'test'}, {'living_space': 'test living space'}]},person)

    def test_that_maximum_no_of_people_is_not_exceeded(self):
        self.dojo.add_person("Neil", "Armstrong", "Staff", "Y")
        self.dojo.add_person("Harry", "Kane", "Fellow", "Y")
        self.dojo.add_person("Eden", "Hazard", "Staff", "Y")
        self.dojo.add_person("Ngolo", "Kante", "Staff", "Y")
        self.dojo.add_person("Eric", "Dier", "Staff", "Y")
        self.dojo.add_person("Dele", "Ali", "Fellow", "Y")
        self.dojo.add_person("Diego", "Costa", "Fellow", "Y")
        self.dojo.add_person("Willian", "Borges", "Staff", "Y")
        self.dojo.add_person("Tibaut", "Courtois", "Fellow", "Y")
        self.assertEqual(len(self.test_office.residents), 6)