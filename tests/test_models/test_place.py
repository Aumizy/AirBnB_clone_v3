#!/usr/bin/python3

""" This file contains test cases for the place module """

import models
import os
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.place import Place
from time import sleep


class TestPlace(unittest.TestCase):
    """Test the Place class."""

    def setUp(self):
        """Creates an instance for place."""
        self.new_place = Place()

    def tearDown(self):
        """Teardown method to run after tests"""
        pass

    def test_place_inheritance(self):
        """Test that the Place class Inherits from BaseModel."""
        self.assertIsInstance(self.new_place, BaseModel)

    def test_place_attributes(self):
        """Check that the attribute exist."""
        attributes = ["city_id", "user_id", "description", "name",
                      "number_rooms", "max_guest", "price_by_night",
                      "latitude", "longitude", "amenity_ids"]
        for attribute in attributes:
            self.assertTrue(attribute in self.new_place.__dir__())

    def test_attribute_types(self):
        """Test types of attributes in the Place class."""
        attribute_types = {
            "amenity_ids": list,
            "longitude": float,
            "latitude": float,
            "price_by_night": int,
            "max_guest": int,
            "number_bathrooms": int,
            "number_rooms": int,
            "description": str,
            "name": str,
            "user_id": str,
            "city_id": str
        }
        for attribute, data_type in attribute_types.items():
            attribute_value = getattr(self.new_place, attribute)
            self.assertIsInstance(attribute_value, data_type)

    def test_str_representation(self):
        """Test the __str__ representation of Place instance."""
        dt = datetime.today()
        dt_repr = repr(dt)
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = dt
        place_str = str(place)
        self.assertIn("[Place] (123456)", place_str)
        self.assertIn("'id': '123456'", place_str)
        self.assertIn("'created_at': " + dt_repr, place_str)
        self.assertIn("'updated_at': " + dt_repr, place_str)

    def test_unused_args(self):
        """Test instantiation of Place with unused args."""
        place = Place(None)
        self.assertNotIn(None, place.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation of Place with kwargs."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        place = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(place.id, "345")
        self.assertEqual(place.created_at, dt)
        self.assertEqual(place.updated_at, dt)

    def test_instantiation_with_none_kwargs(self):
        """Test instantiation of Place with None kwargs."""
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)

    def test_unique_ids(self):
        """Test that two Place instances have unique ids."""
        place1 = Place()
        place2 = Place()
        self.assertNotEqual(place1.id, place2.id)

    def test_different_created_at(self):
        """Test that two Place instances have different created_at values."""
        place1 = Place()
        sleep(0.05)
        place2 = Place()
        self.assertLess(place1.created_at, place2.created_at)

    def test_different_updated_at(self):
        """Test that two Place instances have different updated_at values."""
        place1 = Place()
        sleep(0.05)
        place2 = Place()
        self.assertLess(place1.updated_at, place2.updated_at)

    def test_save_one_instance(self):
        """Test saving one Place instance."""
        place = Place()
        sleep(0.05)
        first_updated_at = place.updated_at
        place.save()
        self.assertLess(first_updated_at, place.updated_at)

    def test_save_two_instances(self):
        """Test saving two Place instances."""
        place = Place()
        sleep(0.05)
        first_updated_at = place.updated_at
        place.save()
        second_updated_at = place.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        place.save()
        self.assertLess(second_updated_at, place.updated_at)

    def test_save_with_argument(self):
        """Test saving Place instance with an argument."""
        place = Place()
        with self.assertRaises(TypeError):
            place.save(None)

    def test_save_updates_file(self):
        """Test saving Place instance updates the file."""
        place = Place()
        place.save()
        place_id = "Place." + place.id
        with open("file.json", "r") as f:
            self.assertIn(place_id, f.read())

    def test_to_dict_type(self):
        """Test that to_dict returns a dictionary."""
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_keys(self):
        """Test that to_dict contains correct keys."""
        place = Place()
        keys = ["id", "created_at", "updated_at", "__class__"]
        for key in keys:
            self.assertIn(key, place.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that to_dict contains added attributes."""
        place = Place()
        place.middle_name = "Holberton"
        place.my_number = 98
        self.assertEqual("Holberton", place.middle_name)
        self.assertIn("my_number", place.to_dict())

    def test_to_dict_datetime_attributes(self):
        """Test that to_dict datetime attributes are strings."""
        place = Place()
        place_dict = place.to_dict()
        self.assertEqual(str, type(place_dict["id"]))
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test that to_dict returns the expected output."""
        dt = datetime.today()
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(place.to_dict(), tdict)

    def test_to_dict_with_argument(self):
        """Test that to_dict with argument raises TypeError."""
        place = Place()
        with self.assertRaises(TypeError):
            place.to_dict(None)


if __name__ == "__main__":
    unittest.main()
