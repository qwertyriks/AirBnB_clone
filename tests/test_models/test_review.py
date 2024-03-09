#!/usr/bin/python3
"""Defines unittests for models/review.py.

"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """Unit testing for testing instantiation of the Review class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        Rv = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(Rv))
        self.assertNotIn("place_id", Rv.__dict__)

    def test_user_id_is_public_class_attribute(self):
        Rv = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(Rv))
        self.assertNotIn("user_id", Rv.__dict__)

    def test_text_is_public_class_attribute(self):
        Rv = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(Rv))
        self.assertNotIn("text", Rv.__dict__)

    def test_two_reviews_unique_ids(self):
        Rv1 = Review()
        Rv2 = Review()
        self.assertNotEqual(Rv1.id, Rv2.id)

    def test_two_reviews_different_created_at(self):
        Rv1 = Review()
        sleep(0.05)
        Rv2 = Review()
        self.assertLess(Rv1.created_at, Rv2.created_at)

    def test_two_reviews_different_updated_at(self):
        Rv1 = Review()
        sleep(0.05)
        Rv2 = Review()
        self.assertLess(Rv1.updated_at, Rv2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        Rv = Review()
        Rv.id = "123456"
        Rv.created_at = Rv.updated_at = dt
        Rvstr = Rv.__str__()
        self.assertIn("[Review] (123456)", Rvstr)
        self.assertIn("'id': '123456'", Rvstr)
        self.assertIn("'created_at': " + dt_repr, Rvstr)
        self.assertIn("'updated_at': " + dt_repr, Rvstr)

    def test_args_unused(self):
        Rv = Review(None)
        self.assertNotIn(None, Rv.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        Rv = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(Rv.id, "345")
        self.assertEqual(Rv.created_at, dt)
        self.assertEqual(Rv.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unit testing for testing save method of the Review class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        Rv = Review()
        sleep(0.05)
        first_updated_at = Rv.updated_at
        Rv.save()
        self.assertLess(first_updated_at, Rv.updated_at)

    def test_two_saves(self):
        Rv = Review()
        sleep(0.05)
        first_updated_at = Rv.updated_at
        Rv.save()
        second_updated_at = Rv.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        Rv.save()
        self.assertLess(second_updated_at, Rv.updated_at)

    def test_save_with_arg(self):
        Rv = Review()
        with self.assertRaises(TypeError):
            Rv.save(None)

    def test_save_updates_file(self):
        Rv = Review()
        Rv.save()
        Rvid = "Review." + Rv.id
        with open("file.json", "r") as f:
            self.assertIn(Rvid, f.read())


class TestReview_to_dict(unittest.TestCase):
    """Unit testing for testing to_dict method of the Review class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        Rv = Review()
        self.assertIn("id", Rv.to_dict())
        self.assertIn("created_at", Rv.to_dict())
        self.assertIn("updated_at", Rv.to_dict())
        self.assertIn("__class__", Rv.to_dict())

    def test_to_dict_contains_added_attributes(self):
        Rv = Review()
        Rv.middle_name = "Holberton"
        Rv.my_number = 98
        self.assertEqual("Holberton", Rv.middle_name)
        self.assertIn("my_number", Rv.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        Rv = Review()
        Rv_dict = Rv.to_dict()
        self.assertEqual(str, type(Rv_dict["id"]))
        self.assertEqual(str, type(Rv_dict["created_at"]))
        self.assertEqual(str, type(Rv_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        Rv = Review()
        Rv.id = "123456"
        Rv.created_at = Rv.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(Rv.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        Rv = Review()
        self.assertNotEqual(Rv.to_dict(), Rv.__dict__)

    def test_to_dict_with_arg(self):
        Rv = Review()
        with self.assertRaises(TypeError):
            Rv.to_dict(None)


if __name__ == "__main__":
    unittest.main()
