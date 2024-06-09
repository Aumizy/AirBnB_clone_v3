#!/usr/bin/python3

""" This file contains all the unittests for the console """

import os
import sys
import unittest
from console import HBNBCommand
from io import StringIO
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from unittest.mock import patch

classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]


class TestConsole(unittest.TestCase):
    """ Comprehensive tests for the console """
    def setUp(self):
        """Set up method to create a console instance for testing"""
        self.console = HBNBCommand()

    def assertOutputContains(self, expected_output, cmd):
        """Helper method to assert output contains the expected string"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd(cmd))
            self.assertIn(expected_output, f.getvalue().strip())

    def test_quit(self):
        """Test quit command"""
        self.assertTrue(self.console.onecmd("quit"))

    def test_EOF(self):
        """Test EOF command"""
        self.assertTrue(self.console.onecmd("EOF"))

    def test_create(self):
        """Test create command"""
        self.assertOutputContains("", "create BaseModel")

    def test_create_missing_class(self):
        """Test create with missing class"""
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(self.console.onecmd("create"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_invalid_class(self):
        """Test create with invalid class"""
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(self.console.onecmd("create MyModel"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_object(self):
        """Test create command for different classes"""
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(self.console.onecmd("create {}"
                                 .format(class_name)))
                self.assertLess(0, len(output.getvalue().strip()))
                test_key = "{}.{}".format(class_name,
                                          output.getvalue().strip())
                self.assertIn(test_key, storage.all().keys())

    def test_show_missing_class(self):
        """Test show with missing class"""
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(self.console.onecmd("show"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_show_invalid_class(self):
        """Test show with invalid class"""
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(self.console.onecmd("show MyModel some_id"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_objects(self):
        """Test destroy with existing objects"""
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(self.console.onecmd("create {}"
                                 .format(class_name)))
                test_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(self.console.onecmd("destroy {} {}"
                                 .format(class_name, test_id)))
                self.assertEqual("", output.getvalue().strip())
                self.assertNotIn("{}.{}".format(class_name, test_id),
                                 storage.all().keys())

    def test_all_invalid_class(self):
        """Test all with invalid class"""
        correct = "** class doesn't exist **"
        self.assertOutputContains(correct, "all MyModel")

    def test_update_missing_class(self):
        """Test update with missing class"""
        correct = "** class name missing **"
        self.assertOutputContains(correct, "update")

    def test_prompt_string(self):
        """Test prompt string"""
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        """Test empty line"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(self.console.onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class TestHelpCommand(unittest.TestCase):
    """Unittests for testing help messages of the interpreter."""

    def test_help_quit(self):
        h = "Quit command used to exit the program"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(h, output.getvalue().strip())


class TestExitCommand(unittest.TestCase):
    """Unittests for testing exiting from the interpreter"""

    def test_quit_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_create(unittest.TestCase):
    """Unittests for testing create from the interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_object(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "BaseModel.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "User.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "State.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "City.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Amenity.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Place.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Review.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())


if __name__ == '__main__':
    unittest.main()
