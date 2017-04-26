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