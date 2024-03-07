#!/usr/bin/python3


import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unit tests for testing instantiation(init) of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        Bm1 = BaseModel()
        Bm2 = BaseModel()
        self.assertNotEqual(Bm1.id, Bm2.id)

    def test_two_models_different_created_at(self):
        Bm1 = BaseModel()
        sleep(0.05)
        Bm2 = BaseModel()
        self.assertLess(Bm1.created_at, Bm2.created_at)

    def test_two_models_different_updated_at(self):
        Bm1 = BaseModel()
        sleep(0.05)
        Bm2 = BaseModel()
        self.assertLess(Bm1.updated_at, Bm2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        Bm = BaseModel()
        Bm.id = "123456"
        Bm.created_at = Bm.updated_at = dt
        Bmstr = Bm.__str__()
        self.assertIn("[BaseModel] (123456)", Bmstr)
        self.assertIn("'id': '123456'", Bmstr)
        self.assertIn("'created_at': " + dt_repr, Bmstr)
        self.assertIn("'updated_at': " + dt_repr, Bmstr)

    def test_args_unused(self):
        Bm = BaseModel(None)
        self.assertNotIn(None, Bm.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        Bm = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(Bm.id, "345")
        self.assertEqual(Bm.created_at, dt)
        self.assertEqual(Bm.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        Bm = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(Bm.id, "345")
        self.assertEqual(Bm.created_at, dt)
        self.assertEqual(Bm.updated_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """Unit tests for testing save() method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

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

    def test_one_save(self):
        Bm = BaseModel()
        sleep(0.05)
        first_updated_at = Bm.updated_at
        Bm.save()
        self.assertLess(first_updated_at, Bm.updated_at)

    def test_two_saves(self):
        Bm = BaseModel()
        sleep(0.05)
        first_updated_at = Bm.updated_at
        Bm.save()
        second_updated_at = Bm.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        Bm.save()
        self.assertLess(second_updated_at, Bm.updated_at)

    def test_save_with_arg(self):
        Bm = BaseModel()
        with self.assertRaises(TypeError):
            Bm.save(None)

    def test_save_updates_file(self):
        Bm = BaseModel()
        Bm.save()
        Bmid = "BaseModel." + Bm.id
        with open("file.json", "r") as f:
            self.assertIn(Bmid, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unit tests for testing to_dict() method of the BaseModel class."""

    def test_to_dict_type(self):
        Bm = BaseModel()
        self.assertTrue(dict, type(Bm.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        Bm = BaseModel()
        self.assertIn("id", Bm.to_dict())
        self.assertIn("created_at", Bm.to_dict())
        self.assertIn("updated_at", Bm.to_dict())
        self.assertIn("__class__", Bm.to_dict())

    def test_to_dict_contains_added_attributes(self):
        Bm = BaseModel()
        Bm.name = "Holberton"
        Bm.my_number = 98
        self.assertIn("name", Bm.to_dict())
        self.assertIn("my_number", Bm.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        Bm = BaseModel()
        Bm_dict = Bm.to_dict()
        self.assertEqual(str, type(Bm_dict["created_at"]))
        self.assertEqual(str, type(Bm_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        Bm = BaseModel()
        Bm.id = "123456"
        Bm.created_at = Bm.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(bm.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        Bm = BaseModel()
        self.assertNotEqual(Bm.to_dict(), Bm.__dict__)

    def test_to_dict_with_arg(self):
        Bm = BaseModel()
        with self.assertRaises(TypeError):
            Bm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
