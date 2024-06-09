#!/usr/bin/python3

""" This file contains all the test cases for the amenity module """

import models
import os
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.amenity import Amenity
from time import sleep


class TestAmenity(unittest.TestCase):
    """Test the Amenity class."""

    def test_amenity_inheritance(self):
        """Test that the Amenity class Inherits from BaseModel."""
        new_amenity = Amenity()
        self.assertIsInstance(new_amenity, BaseModel)

    def test_amenity_attributes(self):
        """Test attributes of the Amenity class."""
        new_amenity = Amenity()
        self.assertTrue("name" in new_amenity.__dir__())

    def test_amenity_attribute_type(self):
        """Test type of the name attribute in Amenity class."""
        new_amenity = Amenity()
        name_value = getattr(new_amenity, "name")
        self.assertIsInstance(name_value, str)

    def test_str_representation(self):
        """Test the __str__ representation of Amenity instance."""
        dt = datetime.today()
        dt_repr = repr(dt)
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = dt
        amenity_str = str(amenity)
        self.assertIn("[Amenity] (123456)", amenity_str)
        self.assertIn("'id': '123456'", amenity_str)
        self.assertIn("'created_at': " + dt_repr, amenity_str)
        self.assertIn("'updated_at': " + dt_repr, amenity_str)

    def test_unused_args(self):
        """Test instantiation of Amenity with unused args."""
        amenity = Amenity(None)
        self.assertNotIn(None, amenity.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation of Amenity with kwargs."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        amenity = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(amenity.id, "345")
        self.assertEqual(amenity.created_at, dt)
        self.assertEqual(amenity.updated_at, dt)

    def test_instantiation_with_none_kwargs(self):
        """Test instantiation of Amenity with None kwargs."""
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

    def test_unique_ids(self):
        """Test that two Amenity instances have unique ids."""
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.id, amenity2.id)

    def test_different_created_at(self):
        """Test that two Amenity instances have different created_at values."""
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.created_at, amenity2.created_at)

    def test_different_updated_at(self):
        """Test that two Amenity instances have different updated_at values."""
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.updated_at, amenity2.updated_at)

    def test_save_one_instance(self):
        """Test saving one Amenity instance."""
        amenity = Amenity()
        sleep(0.05)
        first_updated_at = amenity.updated_at
        amenity.save()
        self.assertLess(first_updated_at, amenity.updated_at)

    def test_save_two_instances(self):
        """Test saving two Amenity instances."""
        amenity = Amenity()
        sleep(0.05)
        first_updated_at = amenity.updated_at
        amenity.save()
        second_updated_at = amenity.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amenity.save()
        self.assertLess(second_updated_at, amenity.updated_at)

    def test_save_with_argument(self):
        """Test saving Amenity instance with an argument."""
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.save(None)

    def test_save_updates_file(self):
        """Test saving Amenity instance updates the file."""
        amenity = Amenity()
        amenity.save()
        amenity_id = "Amenity." + amenity.id
        with open("file.json", "r") as f:
            self.assertIn(amenity_id, f.read())

    def test_to_dict_type(self):
        """Test that to_dict returns a dictionary."""
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_keys(self):
        """Test that to_dict contains correct keys."""
        amenity = Amenity()
        self.assertIn("id", amenity.to_dict())
        self.assertIn("created_at", amenity.to_dict())
        self.assertIn("updated_at", amenity.to_dict())
        self.assertIn("__class__", amenity.to_dict())

    def test_to_dict_added_attributes(self):
        """Test that to_dict contains added attributes."""
        amenity = Amenity()
        amenity.middle_name = "Holberton"
        amenity.my_number = 98
        self.assertEqual("Holberton", amenity.middle_name)
        self.assertIn("my_number", amenity.to_dict())

    def test_to_dict_datetime_attributes(self):
        """Test that to_dict datetime attributes are strings."""
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertEqual(str, type(amenity_dict["id"]))
        self.assertEqual(str, type(amenity_dict["created_at"]))
        self.assertEqual(str, type(amenity_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test that to_dict returns the expected output."""
        dt = datetime.today()
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(amenity.to_dict(), tdict)

    def test_to_dict_with_argument(self):
        """Test that to_dict with argument raises TypeError."""
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.to_dict(None)


if __name__ == "__main__":
    unittest.main()
