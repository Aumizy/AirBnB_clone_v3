#!/usr/bin/python3

""" This file contains all the test cases for the review module """

import models
import os
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.review import Review
from time import sleep


class TestReview(unittest.TestCase):
    """Test the Review class."""

    def setUp(self):
        """Creates an instance for review."""
        self.new_review = Review()

    def tearDown(self):
        pass

    def test_review_inheritance(self):
        """Test that the Review class Inherits from BaseModel."""
        self.assertIsInstance(self.new_review, BaseModel)

    def test_review_attributes(self):
        """Test that Review class has place_id, user_id & text attributes."""
        attributes = ["place_id", "user_id", "text"]
        for attribute in attributes:
            self.assertTrue(attribute in self.new_review.__dir__())

    def test_attribute_types(self):
        """Test types of attributes in the Review class."""
        attribute_types = {
            "place_id": str,
            "user_id": str,
            "text": str
        }
        for attribute, data_type in attribute_types.items():
            attribute_value = getattr(self.new_review, attribute)
            self.assertIsInstance(attribute_value, data_type)

    def test_unused_args(self):
        """Test instantiation of Review with unused args."""
        review = Review(None)
        self.assertNotIn(None, review.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation of Review with kwargs."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        review = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(review.id, "345")
        self.assertEqual(review.created_at, dt)
        self.assertEqual(review.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test instantiation of Review with None kwargs."""
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)

    def test_unique_ids(self):
        """Test that two Review instances have unique ids."""
        review1 = Review()
        review2 = Review()
        self.assertNotEqual(review1.id, review2.id)

    def test_different_created_at(self):
        """Test that two Review instances have different created_at values."""
        review1 = Review()
        sleep(0.05)
        review2 = Review()
        self.assertLess(review1.created_at, review2.created_at)

    def test_different_updated_at(self):
        """Test that two Review instances have different updated_at values."""
        review1 = Review()
        sleep(0.05)
        review2 = Review()
        self.assertLess(review1.updated_at, review2.updated_at)

    def test_save_one_instance(self):
        """Test saving one Review instance."""
        review = Review()
        sleep(0.05)
        first_updated_at = review.updated_at
        review.save()
        self.assertLess(first_updated_at, review.updated_at)

    def test_save_two_instances(self):
        """Test saving two Review instances."""
        review = Review()
        sleep(0.05)
        first_updated_at = review.updated_at
        review.save()
        second_updated_at = review.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        review.save()
        self.assertLess(second_updated_at, review.updated_at)

    def test_save_with_argument(self):
        """Test saving Review instance with an argument."""
        review = Review()
        with self.assertRaises(TypeError):
            review.save(None)

    def test_save_updates_file(self):
        """Test saving Review instance updates the file."""
        review = Review()
        review.save()
        review_id = "Review." + review.id
        with open("file.json", "r") as f:
            self.assertIn(review_id, f.read())

    def test_to_dict_type(self):
        """Test that to_dict returns a dictionary."""
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_keys(self):
        """Test that to_dict contains correct keys."""
        review = Review()
        keys = ["id", "created_at", "updated_at", "__class__"]
        for key in keys:
            self.assertIn(key, review.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that to_dict contains added attributes."""
        review = Review()
        review.middle_name = "Holberton"
        review.my_number = 98
        self.assertEqual("Holberton", review.middle_name)
        self.assertIn("my_number", review.to_dict())

    def test_to_dict_datetime_attributes(self):
        """Test that to_dict datetime attributes are strings."""
        review = Review()
        review_dict = review.to_dict()
        self.assertEqual(str, type(review_dict["id"]))
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test that to_dict returns the expected output."""
        dt = datetime.today()
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(review.to_dict(), tdict)

    def test_to_dict_with_argument(self):
        """Test that to_dict with argument raises TypeError."""
        review = Review()
        with self.assertRaises(TypeError):
            review.to_dict(None)


if __name__ == "__main__":
    unittest.main()
