#!/usr/bin/python3
"""This module contains unittests for the BaseModel class"""

from datetime import datetime
from models.base_model import BaseModel
from models import storage
from time import sleep
import unittest


class TestInstanceType(unittest.TestCase):
    """Test the instance type"""

    def test_isinstance(self):
        b1 = BaseModel()
        self.assertIsInstance(b1, BaseModel)
        self.assertTrue(issubclass(type(b1), BaseModel))


class TestInstanceAttr(unittest.TestCase):
    """Test instance attributes"""

    def test_name(self):
        b1 = BaseModel()
        b1.name = "My First Model"
        self.assertTrue(hasattr(b1, "name"))
        self.assertEqual(b1.name, "My First Model")

    def test_id(self):
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertTrue(hasattr(b1, "id"))
        self.assertIsInstance(b1.id, str)

    def test_universally_uniqueID(self):
        """
        Desc: subTest allows us to run multiple tests in one method
        even if one of them fails. Rather than creating different test cases
        for each instance. it takes in uuid=uuid to provide more context if
        the test fails. e.g
        FAIL: test_uuid (__main__.TestInstanceAttr) (uuid=??notuuidblablabla)
        """
        uuid_list = [BaseModel().id for i in range(2)]
        for uuid in uuid_list:
            with self.subTest(uuid):
                self.assertIs(type(uuid), str)
                self.assertEqual(len(uuid), 36)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')

    def test_uuid_uiniqueness(self):
        uuid_list = [BaseModel().id for i in range(2)]
        # if len of uuid_list is the same as len of the set of it, all unique
        self.assertEqual(len(set(uuid_list)), len(uuid_list))

    def test_isntance_in_storage(self):
        self.assertIn(BaseModel(), storage.all().values())

    def test_created_and_updated_at_types(self):
        b1 = BaseModel()
        self.assertTrue(hasattr(b1, "created_at"))
        self.assertTrue(hasattr(b1, "updated_at"))
        self.assertIsInstance(b1.created_at, datetime)
        self.assertIsInstance(b1.updated_at, datetime)

    def test_datetime_accuracy(self):
        current_date = datetime.now()
        b1 = BaseModel()
        diff = b1.updated_at - b1.created_at
        self.assertTrue(abs(diff.total_seconds()) < 0.01)
        diff = b1.created_at - current_date
        self.assertTrue(abs(diff.total_seconds()) < 0.01)
        self.assertEqual(diff.days, 0)

    def test_str_representation(self):
        b1 = BaseModel()
        b1.id = "12345"
        expected_str = f"[BaseModel] (12345) {b1.__dict__}"

    def test_str_BaseModel(self):
        """test that the str method has the correct output"""
        b1 = BaseModel()
        result = f"[BaseModel] ({b1.id}) {b1.__dict__}"
        self.assertEqual(result, str(b1))

    def test_None_arg(self):
        b1 = BaseModel(None)
        self.assertNotIn(None, b1.__dict__.values())

    def test_kwargs(self):
        created_at_iso = datetime.now().isoformat()
        updated_at_iso = datetime.now().isoformat()
        b1 = BaseModel("12", id="345", created_at=created_at_iso,
                       updated_at=updated_at_iso)
        self.assertEqual(b1.id, "345")
        diff = b1.updated_at - b1.created_at
        self.assertTrue(abs(diff.total_seconds()) < 0.01)

    def test_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)


class TestSaveMethod(unittest.TestCase):
    """Test the save method of the BaseModel"""

    def test_invalid_call(self):
        b1 = BaseModel()
        with self.assertRaises(TypeError):
            b1.save("arg")

    def test_update(self):
        b1 = BaseModel()
        updated_at_creation = b1.updated_at
        b1.save()
        updated_at_save = b1.updated_at
        self.assertNotEqual(updated_at_creation, updated_at_save)

    def test_save_interval(self):
        b1 = BaseModel()
        sleep(0.03)
        creation_time = b1.updated_at
        b1.save()
        self.assertLess(creation_time, b1.updated_at)

    def test_save_twice(self):
        b1 = BaseModel()
        first_updated_at = b1.updated_at
        b1.save()
        second_updated_at = b1.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        b1.save()
        self.assertLess(second_updated_at, b1.updated_at)


class Test_to_dictMethod(unittest.TestCase):
    """Test cases for the to_dict method"""

    def test_arg(self):
        b1 = BaseModel()
        with self.assertRaises(TypeError):
            b1.to_dict("arg")

    def test_None_arg(self):
        b1 = BaseModel()
        with self.assertRaises(TypeError):
            b1.to_dict(None)

    def test_keys_in_dict(self):
        b1 = BaseModel()
        self.assertIn("id", b1.to_dict())
        self.assertIn("created_at", b1.to_dict())
        self.assertIn("updated_at", b1.to_dict())
        self.assertIn("__class__", b1.to_dict())

    def test_retutn_type(self):
        b1 = BaseModel()
        self.assertEqual(dict, type(b1.to_dict()))

    def test_dict_not_to_dict(self):
        b1 = BaseModel()
        to_dict = b1.to_dict()
        self.assertNotEqual(to_dict, b1.__dict__)

    def test_more_attr(self):
        b1 = BaseModel()
        b1.name = "My First Mode"
        b1.my_number = 98
        self.assertIn("name", b1.to_dict())
        self.assertIn("my_number", b1.to_dict())

    def test_date_types(self):
        b1 = BaseModel()
        b1_dict = b1.to_dict()
        self.assertEqual(str, type(b1_dict["created_at"]))
        self.assertEqual(str, type(b1_dict["updated_at"]))

    def test_dictionary(self):
        date = datetime.now()
        b1 = BaseModel()
        b1.id = "98"
        b1.created_at = b1.updated_at = date
        expected_dict = {
            'id': '98',
            '__class__': 'BaseModel',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat()
        }
        self.assertDictEqual(b1.to_dict(), expected_dict)


class TestRecreateInstanceFromDict(unittest.TestCase):
    """Test re-create an instance with this dictionary representation."""

    def test_base_model_dict(self):
        my_model = BaseModel()
        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)
        self.assertIsInstance(my_new_model, BaseModel)
        self.assertIsNot(my_model, my_new_model)


if __name__ == "__main__":
    unittest.main()
