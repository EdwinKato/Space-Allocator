"""Unit tests for the application"""

import colorful
import io
from prettytable import PrettyTable
from src.dojo import Dojo
import sys
import unittest
import os
from src.helpers import get_residents, remove_person, find_room, find_person


class TestSpaceAllocator(unittest.TestCase):
    """ Tests"""

    def setUp(self):
        """ Initial test setup"""

        self.dojo = Dojo()
        self.testoffice = self.dojo.create_room("office", "testoffice")
        self.testlivingspace = self.dojo.create_room(
            "living_space", "testlivingspace")

    def test_create_room(self):
        """Tests that a room is created successfully"""

        initial_room_count = len(self.dojo.rooms)
        blue_office = self.dojo.create_room("office", "Blue")
        self.assertTrue(blue_office)
        new_room_count = len(self.dojo.rooms)
        self.assertEqual(new_room_count - initial_room_count, 1)

    def test_create_room_multiple(self):
        """Tests that multiple rooms are created at a single time successfully"""

        initial_room_count = len(self.dojo.rooms)
        offices = self.dojo.create_room("office", "Blue", "Black", "Brown")
        self.assertTrue(offices)
        new_room_count = len(self.dojo.rooms)
        self.assertEqual(new_room_count - initial_room_count, 3)

    def test_create_room_duplicate(self):
        """Tests that duplicate rooms are not created"""

        initial_room_count = len(self.dojo.people)
        self.testoffice = self.dojo.create_room("office", "testoffice")
        new_room_count = len(self.dojo.people)
        self.assertEqual(new_room_count - initial_room_count, 0)

    def test_add_person(self):
        """Test that person is added to the system"""

        initial_person_count = len(self.dojo.people)
        person = self.dojo.add_person("Neil", "Armstrong", "Staff")
        self.assertTrue(person)
        new_person_count = len(self.dojo.people)
        self.assertEqual(new_person_count - initial_person_count, 1)

    def test_add_person_has_oofice(self):
        """Test that a person is assigned an office"""

        person = self.dojo.add_person("Neil", "Armstrong", "Staff")
        self.assertTrue(person)
        self.assertTrue(self.dojo.people[-1].has_office)

    def test_add_person_has_living_space(self):
        """Test that person is assigned a living space"""

        person = self.dojo.add_person("Eden", "Hazard", "Fellow", "Y")
        self.assertTrue(person)
        self.assertTrue(self.dojo.people[-1].has_living_space)

    def test_add_person_return_type(self):
        """Tests the return type of method add_person"""

        person = self.dojo.add_person("Eden", "Hazard", "Fellow", "Y")
        self.assertEqual(
            {'Person': 'Eden Hazard', 'Rooms': [{'office': 'testoffice'},
                                                {'living_space': 'testlivingspace'}]}, person)

    def test_add_person_maximum(self):
        """Tests that the maximum number of people is not exceeded"""

        self.dojo.add_person("Neil", "Armstrong", "Staff", "Y")
        self.dojo.add_person("Harry", "Kane", "Fellow", "Y")
        self.dojo.add_person("Eden", "Hazard", "Staff", "Y")
        self.dojo.add_person("Ngolo", "Kante", "Staff", "Y")
        self.dojo.add_person("Eric", "Dier", "Staff", "Y")
        self.dojo.add_person("Dele", "Ali", "Fellow", "Y")
        self.dojo.add_person("Diego", "Costa", "Fellow", "Y")
        self.dojo.add_person("Willian", "Borges", "Staff", "Y")
        self.dojo.add_person("Tibaut", "Courtois", "Fellow", "Y")
        self.assertEqual(len(self.testoffice.residents), 6)

    def test_print_room(self):
        """Tests the output of print_room"""

        self.dojo.add_person("Neil", "Armstrong", "Staff", "Y")
        self.dojo.add_person("Harry", "Kane", "Fellow", "Y")
        self.dojo.add_person("Eden", "Hazard", "Staff", "Y")
        self.dojo.add_person("Ngolo", "Kante", "Staff", "Y")
        self.dojo.add_person("Eric", "Dier", "Staff", "Y")
        self.dojo.add_person("Dele", "Ali", "Fellow", "Y")
        self.dojo.add_person("Diego", "Costa", "Fellow", "Y")
        self.dojo.add_person("Willian", "Borges", "Staff", "Y")
        self.dojo.add_person("Tibaut", "Courtois", "Fellow", "Y")
        result = self.dojo.print_room("testoffice")
        non_existent_room = self.dojo.print_room("test room")

        self.assertEqual(
            ['Neil Armstrong', 'Harry Kane', 'Eden Hazard', 'Ngolo Kante',
             'Eric Dier', 'Dele Ali'], result)
        self.assertFalse(non_existent_room)

    def test_reallocate_person(self):
        """Tests that correct information is printed on print_allocations"""

        dojo = Dojo()
        test_office = dojo.create_room("office", "testoffice")
        another_test_office = dojo.create_room("office", "orange")
        dojo.add_person("Neil", "Armstrong", "Staff", "Y")
        person = dojo.people[0]
        old_office = [elem['office']
                      for elem in person.rooms_occupied if 'office' in elem]
        result1 = dojo.print_room(old_office[0])
        self.assertIn("Neil Armstrong", result1)
        un_occupied_room = test_office if not test_office.residents else another_test_office
        print(un_occupied_room.name)
        dojo.reallocate_person(1, un_occupied_room.name)
        result2 = dojo.print_room(old_office[0])
        self.assertNotIn("Neil Armstrong", result2)

    def test_print_allocations(self):
        """Tests the output of print_allocations"""

        self.dojo.add_person("Dele", "Ali", "Fellow", "Y")
        result = self.dojo.print_allocations()
        print(result)
        self.assertEqual([{'testoffice': ['DELE ALI']}, {
            'testlivingspace': ['DELE ALI']}], result)

    def test_print_allocations_on_file(self):
        """Tests that correct output is written to the file
        """

        self.dojo.add_person("Dele", "Ali", "Fellow", "Y")
        result = self.dojo.print_allocations("allocations.txt", "N")
        file = open("allocations.txt").read()
        self.assertTrue("Room: testoffice" in file)
        self.assertTrue("DELE ALI" in file)
        self.assertTrue("Room: testlivingspace" in file)
        self.assertEqual([{'testoffice': ['DELE ALI']}, {
            'testlivingspace': ['DELE ALI']}], result)

    def test_print_allocations_tabular_view(self):
        """Tests that tabular data is output on print_allocations"""

        # Create StringIO object and redirect output
        self.dojo.add_person("Dele", "Ali", "Fellow", "Y")
        program_captured_output = io.StringIO()
        sys.stdout = program_captured_output
        self.dojo.print_allocations("", "Y")
        sys.stdout = sys.__stdout__
        table = PrettyTable(['Name', 'Type', 'Office', 'Living Space'])
        table.add_row(["Dele Ali", "fellow", "testoffice", "testlivingspace"])

        captured_output = io.StringIO()
        sys.stdout = captured_output
        print(colorful.blue("List showing people with space and their respective rooms"))
        print(colorful.blue(table))
        sys.stdout = sys.__stdout__
        print(program_captured_output.getvalue().strip())
        print(captured_output.getvalue())
        self.assertTrue(captured_output.getvalue().strip()
                        in program_captured_output.getvalue().strip())

    def test_print_unallocated_tabular(self):
        """Tests that tabular data is output on test_tabular_output_on_print_unallocated"""

        dojo = Dojo()
        dojo.add_person("Kylian", "Mbappe", "Fellow", "Y")
        dojo.add_person("Gianluggi", "Buffon", "Fellow", "N")
        dojo.create_room("office", "red")
        dojo.add_person("Timoue", "Bakayoko", "Fellow", "Y")
        program_captured_output = io.StringIO()
        sys.stdout = program_captured_output
        dojo.print_unallocated()
        sys.stdout = sys.__stdout__
        table = PrettyTable(['Name', 'Person id', 'Missing'])
        table.add_row(["Kylian Mbappe", "1", "Office and Living Space"])
        table.add_row(["Gianluggi Buffon", "2", "Office"])
        table.add_row(["Timoue Bakayoko", "3", "Living Space"])

        captured_output = io.StringIO()
        sys.stdout = captured_output
        print(colorful.blue("Table showing people along with missing rooms"))
        print(colorful.blue(table))
        sys.stdout = sys.__stdout__
        print(program_captured_output.getvalue().strip())
        print(captured_output.getvalue())
        self.assertTrue(captured_output.getvalue().strip()
                        in program_captured_output.getvalue().strip())

    def test_reallocate_person_no_office(self):
        """Tests reallocate if person had no office"""

        dojo = Dojo()
        dojo.add_person("John", "Ashaba", "Staff", "Y")
        dojo.create_room("office", "orange")
        dojo.reallocate_person(1, "orange")
        target_room = find_room(dojo.rooms, "orange")
        person = find_person(dojo.people, 1)
        self.assertIn(person, target_room.residents)

    def test_reallocate_person_no_living_space(self):
        """Tests reallocate if person had no living space"""

        self.dojo.add_person("John", "Ashaba", "Staff", "Y")
        self.dojo.create_room("living_space", "gorrilla")
        self.dojo.reallocate_person(1, "gorrilla")
        target_room = find_room(self.dojo.rooms, "gorrilla")
        person = find_person(self.dojo.people, 1)
        self.assertIn(person, target_room.residents)

    def test_load_people(self):
        """Tests that person exists after load_people"""

        self.dojo.load_people("resources/people.txt")
        last_person = find_person(self.dojo.people, 7)
        self.assertIn(last_person, self.dojo.people)

    def test_if_person_exists_in_target_room_after_reallocation(self):
        """Tests that person exists after reallocation"""

        self.dojo.create_room("office", "orange")
        self.dojo.create_room("living_space", "lion")
        self.dojo.add_person("John", "Ashaba", "Fellow", "Y")
        person = self.dojo.people[0]
        old_office = [elem['office']
                      for elem in person.rooms_occupied if 'office' in elem]
        old_living_space = [
            elem['living_space']
            for elem in person.rooms_occupied if 'living_space' in elem]
        result1 = self.dojo.print_room(old_office[0])
        result2 = self.dojo.print_room(old_living_space[0])
        self.assertIn("John Ashaba", result1)
        self.assertIn("John Ashaba", result2)
        self.dojo.reallocate_person(1, "orange")
        self.dojo.reallocate_person(1, "lion")
        target_office_room = find_room(self.dojo.rooms, "orange")
        target_living_room = find_room(self.dojo.rooms, "orange")
        person = find_person(self.dojo.people, 1)
        self.assertIn(person, target_office_room.residents)
        self.assertIn(person, target_living_room.residents)

    def test_persists_data(self):
        """Tests that the application persists data"""

        dojo1 = Dojo()
        dojo1.create_room("office", "orange")
        dojo1.add_person("John", "Ashaba", "Staff", "Y")
        if os.path.exists("resources/testdb.db"):
            os.remove("resources/testdb.db")
        dojo1.save_state("testdb.db")
        dojo2 = Dojo()
        dojo2.load_state("resources/testdb.db")
        room = find_room(dojo2.rooms, "orange")
        self.assertIn(room, dojo2.rooms)
