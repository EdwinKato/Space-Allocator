import unittest
import io
import sys
import colorful
from prettytable import PrettyTable
from src.dojo import Dojo


class TestSpaceAllocator(unittest.TestCase):
    """class
    """

    def setUp(self):
        self.dojo = Dojo()
        self.testOffice = self.dojo.create_room("office", "testOffice")
        self.testLivingSpace = self.dojo.create_room("living_space", "testLivingSpace")

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
        self.assertEqual(
            {'Person': 'Eden Hazard', 'Rooms': [{'office': 'testOffice'}, \
            {'living_space': 'testLivingSpace'}]}, person)

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
        self.assertEqual(len(self.testOffice.residents), 6)

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
        result = self.dojo.print_room("testOffice")
        non_existent_room = self.dojo.print_room("test room")

        self.assertEqual(
            ['Neil Armstrong', 'Harry Kane', 'Eden Hazard', 'Ngolo Kante',\
            'Eric Dier', 'Dele Ali'], result)
        self.assertFalse(non_existent_room)

    def test_print_room_for_reallocated_people(self):
        self.dojo.create_room("office", "orange")
        self.dojo.add_person("Neil", "Armstrong", "Staff", "Y")
        result1 = self.dojo.print_room("testOffice")
        self.assertIn("Neil Armstrong", result1)
        self.dojo.reallocate_person(1, "orange")
        result2 = self.dojo.print_room("testOffice")
        self.assertNotIn("Neil Armstrong", result2)

    def test_correct_output_on_print_allocations(self):
        self.dojo.add_person("Dele", "Ali", "Fellow", "Y")
        result = self.dojo.print_allocations()
        print(result)
        self.assertEqual(
            [{'testOffice': ['DELE ALI']}, {'testLivingSpace': ['DELE ALI']}], result)

    def test_print_allocations_on_file(self):
        """Tests that correct output is written to the file
        """

        self.dojo.add_person("Dele", "Ali", "Fellow", "Y")
        result = self.dojo.print_allocations("allocations.txt", "N")
        file = open("allocations.txt").read()
        self.assertTrue("Room: testOffice" in file)
        self.assertTrue("DELE ALI" in file)
        self.assertTrue("Room: testLivingSpace" in file)
        self.assertEqual(
            [{'testOffice': ['DELE ALI']}, {'testLivingSpace': ['DELE ALI']}], result)

    def test_tabular_output_on_print_allocations(self):
        """Tests that print_allocations output is tabular
        """

        #Create StringIO object and redirect output
        self.dojo.add_person("Dele", "Ali", "Fellow", "Y")
        program_captured_output = io.StringIO()
        sys.stdout = program_captured_output
        self.dojo.print_allocations("", "Y")
        sys.stdout = sys.__stdout__
        table = PrettyTable(['Name', 'Type', 'Office', 'Living Space'])
        table.add_row(["Dele Ali", "fellow", "testOffice", "testLivingSpace"])

        captured_output = io.StringIO()
        sys.stdout = captured_output
        print(colorful.blue("List showing people with space and their respective rooms"))
        print(colorful.blue(table))
        sys.stdout = sys.__stdout__
        print(program_captured_output.getvalue().strip())
        print(captured_output.getvalue())
        self.assertTrue(
            captured_output.getvalue().strip() in program_captured_output.getvalue().strip())

    def test_correct_output_on_print_unallocated(self):
        """test
        """

        dojo = Dojo()
        dojo.add_person("Kylian", "Mbappe", "Fellow", "Y")
        # dojo.create_room("living_space", "zebra")
        # dojo.add_person("Gonzalo", "Higuan", "Fellow", "Y")
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
        self.assertTrue(
            captured_output.getvalue().strip() in program_captured_output.getvalue().strip())

    def test_reallocate_if_person_had_no_office(self):
        """test
        """
        dojo = Dojo()
        dojo.add_person("John", "Ashaba", "Staff", "Y")
        dojo.create_room("office", "orange")
        dojo.reallocate_person(1, "orange")
        target_room = dojo.find_room("orange")
        person = dojo.find_person(1)
        self.assertIn(person, target_room.residents)

    def test_reallocate_if_person_had_no_living_space(self):
        """test
        """
        dojo = Dojo()
        dojo.add_person("John", "Ashaba", "Staff", "Y")
        dojo.create_room("living_space", "gorrilla")
        dojo.reallocate_person(1, "gorrilla")
        target_room = dojo.find_room("gorrilla")
        person = dojo.find_person(1)
        self.assertIn(person, target_room.residents)

    def test_person_exists_after_load_people(self):
        """test
        """

        self.dojo.load_people("people.txt")
        last_person = self.dojo.find_person(7)
        self.assertIn(last_person, self.dojo.all_people)

    def test_person_exists_in_target_room_after_reallocation(self):
        """test
        """

        self.dojo.create_room("office", "orange")
        self.dojo.create_room("living_space", "lion")
        self.dojo.add_person("John", "Ashaba", "Fellow", "Y")
        result1 = self.dojo.print_room("testOffice")
        result2 = self.dojo.print_room("testLivingSpace")
        self.assertIn("John Ashaba", result1)
        self.assertIn("John Ashaba", result2)
        self.dojo.reallocate_person(1, "orange")
        self.dojo.reallocate_person(1, "lion")
        target_office_room = self.dojo.find_room("orange")
        target_living_room = self.dojo.find_room("orange")
        person = self.dojo.find_person(1)
        self.assertIn(person, target_office_room.residents)
        self.assertIn(person, target_living_room.residents)

    def test_persists_data(self):
        """test
        """

        dojo1 = Dojo()
        dojo1.create_room("office", "orange")
        dojo1.add_person("John", "Ashaba", "Staff", "Y")
        dojo1.save_state("mydb.db")
        dojo2 = Dojo()
        dojo2.load_state("mydb.db")
        room = dojo2.find_room("orange")
        self.assertIn(room, dojo2.all_rooms)
