#!/usr/bin/python3
"""This file contains the user module test cases"""

import os
import unittest
from datetime import datetime
from models import storage
from models.base_model import BaseModel
from models.user import User
from time import sleep


class TestUser(unittest.TestCase):
    """Test cases for the User class."""

    @classmethod
    def setUpClass(cls):
        """Setup class to create temporary file."""
        cls.user_data_file = 'file.json'
        cls.backup_data_file = 'file_backup.json'
        cls.user = User()
        storage.save()

    @classmethod
    def tearDownClass(cls):
        """Teardown class to clean up temporary files."""
        try:
            os.rename(cls.backup_data_file, cls.user_data_file)
        except FileNotFoundError:
            pass

    def test_inheritance_and_attributes(self):
        """Test inheritance and basic attributes."""
        self.assertIsInstance(self.user, BaseModel)

        attributes = ["email", "first_name", "last_name", "password"]
        for attribute in attributes:
            self.assertTrue(hasattr(self.user, attribute))

        self.assertIsInstance(self.user.email, str)
        self.assertIsInstance(self.user.first_name, str)
        self.assertIsInstance(self.user.last_name, str)
        self.assertIsInstance(self.user.password, str)

    def test_created_at_and_updated_at(self):
        """Test created_at and updated_at attributes."""
        self.assertIsInstance(self.user.created_at, datetime)
        self.assertIsInstance(self.user.updated_at, datetime)

    def test_save_updates_updated_at(self):
        """Test that calling save updates the updated_at attribute."""
        old_updated_at = self.user.updated_at
        self.user.save()
        new_updated_at = self.user.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)

    def test_str_representation(self):
        """Test the __str__ representation of User instance."""
        user_str = str(self.user)
        self.assertIn("[User]", user_str)
        self.assertIn("'id':", user_str)
        self.assertIn("'created_at':", user_str)
        self.assertIn("'updated_at':", user_str)

    def test_to_dict_method(self):
        """Test the to_dict method of User instance."""
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict['__class__'], 'User')
        self.assertEqual(user_dict['id'], str(self.user.id))
        self.assertEqual(user_dict['created_at'],
                         self.user.created_at.isoformat())
        self.assertEqual(user_dict['updated_at'],
                         self.user.updated_at.isoformat())

    def test_user_delete(self):
        """Test deleting User instance."""
        user_id = self.user.id
        self.user.save()
        storage.reload()

        self.assertNotIn(user_id, storage.all())

        storage.delete(self.user)
        storage.save()

        storage.reload()
        self.assertNotIn(user_id, storage.all())

    def test_user_attributes_after_reload(self):
        """
        Test that User instance attributes remain
        consistent after reload.
        """
        user_id = self.user.id
        user_created_at = self.user.created_at
        user_updated_at = self.user.updated_at

        self.user.save()
        self.user.email = 'new_email@example.com'
        self.user.first_name = 'John'
        self.user.save()

        storage.reload()
        reloaded_user = storage.all()[f"User.{user_id}"]

        self.assertEqual(reloaded_user.email, 'new_email@example.com')
        self.assertEqual(reloaded_user.first_name, 'John')
        self.assertEqual(reloaded_user.created_at, user_created_at)
        self.assertNotEqual(reloaded_user.updated_at, user_updated_at)

    def test_instantiation(self):
        """Test instantiation with different arguments."""
        self.assertEqual(User, type(User()))
        self.assertIn(User(), storage.all().values())
        self.assertEqual(str, type(User().id))
        self.assertEqual(datetime, type(User().created_at))
        self.assertEqual(datetime, type(User().updated_at))
        self.assertEqual(str, type(User.email))
        self.assertEqual(str, type(User.password))
        self.assertEqual(str, type(User.first_name))
        self.assertEqual(str, type(User.last_name))
        self.assertNotEqual(User(), User())

    def test_str_representation_with_custom_id(self):
        """Test __str__ representation with a custom ID."""
        dt = datetime.today()
        dt_repr = repr(dt)
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = dt
        usstr = us.__str__()
        self.assertIn("[User] (123456)", usstr)
        self.assertIn("'id': '123456'", usstr)
        self.assertIn("'created_at': " + dt_repr, usstr)
        self.assertIn("'updated_at': " + dt_repr, usstr)

    def test_instantiation_with_kwargs(self):
        """Test instantiation with kwargs."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        us = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(us.id, "345")
        self.assertEqual(us.created_at, dt)
        self.assertEqual(us.updated_at, dt)

        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

    def test_saves(self):
        """Test save method."""
        us = User()
        sleep(0.05)
        first_updated_at = us.updated_at
        us.save()
        self.assertLess(first_updated_at, us.updated_at)

        sleep(0.05)
        second_updated_at = us.updated_at
        us.save()
        self.assertLess(second_updated_at, us.updated_at)

        with self.assertRaises(TypeError):
            us.save(None)

        us.save()
        usid = "User." + us.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())

    def test_to_dict(self):
        """Test to_dict method."""
        dt = datetime.today()
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }

        self.assertDictEqual(us.to_dict(), tdict)


if __name__ == "__main__":
    unittest.main()
