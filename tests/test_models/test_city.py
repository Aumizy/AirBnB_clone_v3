#!/usr/bin/python3

""" This file contains all the test cases for the city module """

import models
import os
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.city import City
from time import sleep


class TestCity(unittest.TestCase):
    """Test the City class."""

    def test_city_inheritance(self):
        """Test that the City class Inherits from BaseModel."""
        new_city = City()
        self.assertIsInstance(new_city, BaseModel)

    def test_city_attributes(self):
        """Test attributes of the City class."""
        new_city = City()
        self.assertTrue("state_id" in new_city.__dir__())
        self.assertTrue("name" in new_city.__dir__())

    def test_type_name(self):
        """Test the type of name attribute."""
        new_city = City()
        name = getattr(new_city, "name")
        self.assertIsInstance(name, str)

    def test_type_state_id(self):
        """Test the type of state_id attribute."""
        new_city = City()
        state_id = getattr(new_city, "state_id")
        self.assertIsInstance(state_id, str)

    def test_str_representation(self):
        """Test the __str__ representation of City instance."""
        dt = datetime.today()
        dt_repr = repr(dt)
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = dt
        city_str = str(city)
        self.assertIn("[City] (123456)", city_str)
        self.assertIn("'id': '123456'", city_str)
        self.assertIn("'created_at': " + dt_repr, city_str)
        self.assertIn("'updated_at': " + dt_repr, city_str)

    def test_unused_args(self):
        """Test instantiation of City with unused args."""
        city = City(None)
        self.assertNotIn(None, city.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation of City with kwargs."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        city = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(city.id, "345")
        self.assertEqual(city.created_at, dt)
        self.assertEqual(city.updated_at, dt)

    def test_instantiation_with_none_kwargs(self):
        """Test instantiation of City with None kwargs."""
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)

    def test_unique_ids(self):
        """Test that two City instances have unique ids."""
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def test_different_created_at(self):
        """Test that two City instances have different created_at values."""
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.created_at, city2.created_at)

    def test_different_updated_at(self):
        """Test that two City instances have different updated_at values."""
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.updated_at, city2.updated_at)

    def test_save_one_instance(self):
        """Test saving one City instance."""
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        self.assertLess(first_updated_at, city.updated_at)

    def test_save_two_instances(self):
        """Test saving two City instances."""
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        second_updated_at = city.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city.save()
        self.assertLess(second_updated_at, city.updated_at)

    def test_save_with_argument(self):
        """Test saving City instance with an argument."""
        city = City()
        with self.assertRaises(TypeError):
            city.save(None)

    def test_save_updates_file(self):
        """Test saving City instance updates the file."""
        city = City()
        city.save()
        city_id = "City." + city.id
        with open("file.json", "r") as f:
            self.assertIn(city_id, f.read())

    def test_to_dict_type(self):
        """Test that to_dict returns a dictionary."""
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_keys(self):
        """Test that to_dict contains correct keys."""
        city = City()
        self.assertIn("id", city.to_dict())
        self.assertIn("created_at", city.to_dict())
        self.assertIn("updated_at", city.to_dict())
        self.assertIn("__class__", city.to_dict())

    def test_to_dict_added_attributes(self):
        """Test that to_dict contains added attributes."""
        city = City()
        city.middle_name = "Holberton"
        city.my_number = 98
        self.assertEqual("Holberton", city.middle_name)
        self.assertIn("my_number", city.to_dict())

    def test_to_dict_datetime_attributes(self):
        """Test that to_dict datetime attributes are strings."""
        city = City()
        city_dict = city.to_dict()
        self.assertEqual(str, type(city_dict["id"]))
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test that to_dict returns the expected output."""
        dt = datetime.today()
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(city.to_dict(), tdict)

    def test_to_dict_with_argument(self):
        """Test that to_dict with argument raises TypeError."""
        city = City()
        with self.assertRaises(TypeError):
            city.to_dict(None)


if __name__ == "__main__":
    unittest.main()
