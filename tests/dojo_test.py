import unittest
from src.dojo import Dojo


class TestCreateRoom (unittest.TestCase):

    def setUp(self):
        self.dojo = Dojo()
        self.test_office = self.dojo.create_room("office", "test")
        self.test_living_space = self.dojo.create_room("living_space", "test living space")

    def test_create_room_successfully(self):
        initial_room_count = len(self.dojo.all_rooms)
        blue_office = self.dojo.create_room("office", "Blue")
        self.assertTrue(blue_office)
        new_room_count = len(self.dojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 1)

    def test_create_rooms_successfully(self):
        initial_room_count = len(self.dojo.all_rooms)
        offices = self.dojo.create_room("office", "Blue", "Black", "Brown")
        self.assertTrue(offices)
        new_room_count = len(self.dojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 3)
        
    def test_addition_of_duplicate_room_names(self):
        initial_room_count = len(self.dojo.all_people)
        room1 = self.dojo.create_room("office", "Blue")
        room1 = self.dojo.create_room("office", "Blue")
        new_room_count = len(self.dojo.all_people)
        self.assertEqual(new_room_count - initial_room_count, 0)

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

    def test_output_of_print_room(self):
        self.dojo.add_person("Neil", "Armstrong", "Staff", "Y")
        self.dojo.add_person("Harry", "Kane", "Fellow", "Y")
        self.dojo.add_person("Eden", "Hazard", "Staff", "Y")
        self.dojo.add_person("Ngolo", "Kante", "Staff", "Y")
        self.dojo.add_person("Eric", "Dier", "Staff", "Y")
        self.dojo.add_person("Dele", "Ali", "Fellow", "Y")
        self.dojo.add_person("Diego", "Costa", "Fellow", "Y")
        self.dojo.add_person("Willian", "Borges", "Staff", "Y")
        self.dojo.add_person("Tibaut", "Courtois", "Fellow", "Y")
        result = self.dojo.print_room("test")
        self.assertEqual(['Neil Armstrong', 'Harry Kane', 'Eden Hazard', 'Ngolo Kante', 'Eric Dier', 'Dele Ali'], result)

    def test_print_room_for_reallocated_people(self):
        self.dojo.create_room("office", "orange")
        self.dojo.add_person("Neil", "Armstrong", "Staff", "Y")
        result1 = self.dojo.print_room("test")
        self.assertIn("Neil Armstrong", result1)
        self.dojo.reallocate_person(1, "orange")
        result2 = self.dojo.print_room("test")
        self.assertNotIn("Neil Armstrong", result2)

    def test_correct_output_on_print_allocations(self):
        self.dojo.add_person("Dele", "Ali", "Fellow", "Y")
        result = self.dojo.print_allocations()
        print(result)
        self.assertEqual([{'test': ['DELE ALI']}, {'test living space': ['DELE ALI']}], result)

    def test_correct_output_on_print_unallocated(self):
        self.dojo.add_person("Dele", "Ali", "Fellow", "Y")
        result = self.dojo.print_allocations()
        print(result)
        self.assertEqual([{'test': ['DELE ALI']}, {'test living space': ['DELE ALI']}], result)
        
    def test_person_exists_after_load_people(self):
        self.dojo.load_people("../people.txt")
        last_person = self.dojo.find_person(7)
        self.assertIn(last_person,self.dojo.all_people)

    def test_person_exists_in_target_room(self):
        self.dojo.create_room("office", "orange")
        self.dojo.add_person("John", "Ashaba", "Staff", "Y")
        result1 = self.dojo.print_room("test")
        self.assertIn("John Ashaba", result1)
        self.dojo.reallocate_person(1, "orange")
        target_room = self.dojo.find_room("orange")
        person = self.dojo.find_person(1)
        self.assertIn(person, target_room.residents)