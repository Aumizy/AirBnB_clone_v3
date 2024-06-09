#!/usr/bin/python3

""" This file contains the test cases for the state module """

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
from models.state import State


class TestState(unittest.TestCase):
    """ Tests for the state class """

    @classmethod
    def setUpClass(cls):
        """Setup class to create temporary file."""
        cls.state_data_file = 'file.json'
        cls.backup_data_file = 'file_backup.json'
        cls.state = State()
        models.storage.save()

    @classmethod
    def tearDownClass(cls):
        """Teardown class to clean up temporary files."""
        try:
            os.rename(cls.backup_data_file, cls.state_data_file)
        except FileNotFoundError:
            pass

    @classmethod
    def from_dict(cls, data):
        """Create a new instance of State from a dictionary."""
        new_state = cls()
        for key, value in data.items():
            if key != '__class__':
                setattr(new_state, key, value)
        return new_state

    def test_state_inheritence(self):
        """Test that State class inherits from BaseModel."""
        self.assertIsInstance(self.state, BaseModel)

    def test_state_attributes(self):
        """Test the presence of specific attributes in State instance."""
        self.assertTrue("name" in self.state.__dir__())

    def test_state_attributes_type(self):
        """Test the types of attributes in State instance."""
        name = getattr(self.state, "name")
        self.assertIsInstance(name, str)

    def test_default_values(self):
        """Test that default values are set correctly."""
        new_state = State()
        self.assertEqual(new_state.name, "")

    def test_name_assignment(self):
        """Test setting and getting the name attribute."""
        new_state = State()
        new_state.name = "Lagos"
        self.assertEqual(new_state.name, "Lagos")

    def test_created_at_update_on_save(self):
        """Test that the 'created_at' attribute is not updated on save."""
        new_state = State()
        created_at_before = new_state.created_at
        new_state.save()
        self.assertEqual(new_state.created_at, created_at_before)

    def test_updated_at_update_on_save(self):
        """Test that the 'updated_at' attribute is updated on save."""
        new_state = State()
        updated_at_before = new_state.updated_at
        new_state.save()
        self.assertNotEqual(new_state.updated_at, updated_at_before)

    def test_updated_at_greater_than_created_at(self):
        """Test that 'updated_at' is always greater than 'created_at'."""
        new_state = State()
        self.assertLess(new_state.created_at, new_state.updated_at)

    def test_to_dict_method(self):
        """Test the to_dict method for correctness."""
        dt = datetime.today()
        new_state = State()
        new_state.id = "987654"
        new_state.name = "Lagos"
        new_state.created_at = new_state.updated_at = dt
        state_dict = new_state.to_dict()

        self.assertEqual(state_dict['id'], '987654')
        self.assertEqual(state_dict['name'], 'Lagos')
        self.assertEqual(state_dict['__class__'], 'State')
        self.assertEqual(state_dict['created_at'], dt.isoformat())
        self.assertEqual(state_dict['updated_at'], dt.isoformat())

    def test_instantiation(self):
        """Test instantiation of State class with various arguments."""
        st = State()
        self.assertEqual(State, type(State()))
        self.assertIn(st, models.storage.all().values())
        self.assertEqual(str, type(State().id))
        self.assertEqual(datetime, type(State().created_at))
        self.assertEqual(datetime, type(State().updated_at))

    def test_two_states_unique_ids(self):
        """Test that two instances of State have unique ids."""
        st1 = State()
        st2 = State()
        self.assertNotEqual(st1.id, st2.id)

    def test_two_states_different_created_at(self):
        """Test that two instances of State have different created_at."""
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.created_at, st2.created_at)

    def test_two_states_different_updated_at(self):
        """Test that two instances of State have different updated_at."""
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.updated_at, st2.updated_at)

    def test_str_representation(self):
        """Test the __str__ representation of State instance."""
        dt = datetime.today()
        dt_repr = repr(dt)
        st = State()
        st.id = "123456"
        st.created_at = st.updated_at = dt
        ststr = st.__str__()
        self.assertIn("[State] (123456)", ststr)
        self.assertIn("'id': '123456'", ststr)
        self.assertIn("'created_at': " + dt_repr, ststr)
        self.assertIn("'updated_at': " + dt_repr, ststr)

    def test_args_unused(self):
        """Test that State instance is created even with unused arguments."""
        st = State(None)
        self.assertNotIn(None, st.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test that State instance can be instantiated with kwargs."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        st = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(st.id, "345")
        self.assertEqual(st.created_at, dt)
        self.assertEqual(st.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test that State instance cannot be instantiated with None kwargs."""
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)

    def test_one_save(self):
        """Test that calling save updates the updated_at attribute."""
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        new_updated_at = st.updated_at
        self.assertNotEqual(first_updated_at, new_updated_at)

    def test_two_saves(self):
        """Test that calling save updates the updated_at attribute."""
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        second_updated_at = st.updated_at
        self.assertNotEqual(first_updated_at, second_updated_at)
        sleep(0.05)
        st.save()
        new_updated_at = st.updated_at
        self.assertNotEqual(second_updated_at, new_updated_at)

    def test_save_with_arg(self):
        """Test that save method does not accept arguments."""
        st = State()
        with self.assertRaises(TypeError):
            st.save(None)

    def test_save_updates_file(self):
        """Test that calling save updates the storage file."""
        st = State()
        st.save()
        st_id = "State." + st.id
        with open("file.json", "r") as f:
            self.assertIn(st_id, f.read())

    def test_to_dict_type(self):
        """Test the to_dict method returns a dictionary."""
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that to_dict method contains the correct keys."""
        st = State()
        self.assertIn("id", st.to_dict())
        self.assertIn("created_at", st.to_dict())
        self.assertIn("updated_at", st.to_dict())
        self.assertIn("__class__", st.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that to_dict method contains added attributes."""
        st = State()
        st.middle_name = "Holberton"
        st.my_number = 98
        self.assertEqual("Holberton", st.middle_name)
        self.assertIn("my_number", st.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that to_dict method returns datetime attributes as strings."""
        st = State()
        st_dict = st.to_dict()
        self.assertEqual(str, type(st_dict["id"]))
        self.assertEqual(str, type(st_dict["created_at"]))
        self.assertEqual(str, type(st_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of to_dict method."""
        dt = datetime.today()
        st = State()
        st.id = "123456"
        st.created_at = st.updated_at = dt
        t_dict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(st.to_dict(), t_dict)

    def test_contrast_to_dict_dunder_dict(self):
        """Test that the output of to_dict is different from __dict__."""
        st = State()
        self.assertNotEqual(st.to_dict(), st.__dict__)

    def test_to_dict_with_arg(self):
        """Test that to_dict method does not accept arguments."""
        st = State()
        with self.assertRaises(TypeError):
            st.to_dict(None)


if __name__ == "__main__":
    unittest.main()
