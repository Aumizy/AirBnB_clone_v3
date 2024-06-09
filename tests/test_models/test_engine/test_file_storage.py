#!/usr/bin/python3
"""This module contains Tests for the FileStorage class"""

from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
import json
import os
import unittest


class TestFileStorage(unittest.TestCase):
    """Test the File storage instances"""

    my_model = BaseModel()

    def test_IsInstance(self):
        self.assertIsInstance(storage, FileStorage)

    def test_storage_methods(self):
        self.my_model.full_name = "my_model"
        self.my_model.save()
        bm_dict = self.my_model.to_dict()
        all_objs = storage.all()

        key = bm_dict['__class__'] + "." + bm_dict['id']
        self.assertEqual(key in all_objs, True)

    def test_storage_update_methods(self):
        self.my_model.my_name = "First name"
        self.my_model.save()
        bm_dict = self.my_model.to_dict()
        all_objs = storage.all()

        key = bm_dict['__class__'] + "." + bm_dict['id']

        self.assertEqual(key in all_objs, True)
        self.assertEqual(bm_dict['my_name'], "First name")

        create1 = bm_dict['created_at']
        update1 = bm_dict['updated_at']

        self.my_model.my_name = "Second name"
        self.my_model.save()
        bm_dict = self.my_model.to_dict()
        all_objs = storage.all()

        self.assertEqual(key in all_objs, True)

        create2 = bm_dict['created_at']
        update2 = bm_dict['updated_at']

        self.assertEqual(create1, create2)
        self.assertNotEqual(update1, update2)
        self.assertEqual(bm_dict['my_name'], "Second name")

    def test_attr(self):
        self.assertEqual(hasattr(FileStorage, '_FileStorage__file_path'), True)
        self.assertEqual(hasattr(FileStorage, '_FileStorage__objects'), True)

    def test_save_file(self):
        self.my_model.save()
        self.assertEqual(os.path.exists(storage._FileStorage__file_path), True)
        self.assertEqual(storage.all(), storage._FileStorage__objects)

    def test_reload(self):
        self.my_model.save()
        self.assertTrue(os.path.exists(storage._FileStorage__file_path))

        dict_obj = storage.all()
        FileStorage._FileStorage__objects.clear()
        storage.reload()

        reloaded_keys = storage.all().keys()
        self.assertCountEqual(dict_obj.keys(), reloaded_keys)

        for key in dict_obj.keys():
            self.assertEqual(dict_obj[key].to_dict(),
                             storage.all()[key].to_dict())

    def testSaveSelf(self):
        with self.assertRaises(TypeError) as e:
            FileStorage.save(self, 100)


if __name__ == "__main__":
    unittest.main()
