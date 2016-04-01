from unittest import TestCase

from directory.models import Person
from directory.scraper import (get_person,
                               get_search_inputs,
                               get_results)
from directory.helpers import (search_field_aliases,
                               search_field_full_name,
                               valid_department,
                               valid_person_type)
from directory.search import Search
from directory import search
from directory.exceptions import DirectoryValidationException


class PersonTests(TestCase):
    def test_set_key_init(self):
        person = Person(webid='1')
        self.assertEqual(person.webid, '1')

    def test_setter(self):
        person = Person()
        person.webid = '1'
        self.assertEqual(person.webid, '1')

    def test_str(self):
        person = Person(webid='1')
        self.assertEqual(str(person), '<Person 1>')

    def test_repr(self):
        person = Person(webid='1')
        self.assertEqual(repr(person), '<Person 1>')


class HelperTests(TestCase):
    def test_search_field_full_name(self):
        fields = {'ctl00$ctl00$PageContent$PageContent$middDirectoryForm$txtTelephonenumber': ''}  # noqa
        full = search_field_full_name(fields.keys(), 'phone')

        self.assertIn(full, fields)

    def test_valid_person_type(self):
        invalid = 'notaperson'
        self.assertFalse(valid_person_type(invalid))

        valid = 'Student'
        self.assertTrue(valid_person_type(valid))

        valid_aliased = 'Summer Graduate'
        self.assertTrue(valid_person_type(valid_aliased))

    def test_valid_department(self):
        valid = 'Russian School'
        self.assertTrue(valid_department(valid))

        invalid = 'Not A Department'
        self.assertFalse(valid_department(invalid))


class ScraperTests(TestCase):
    def test_get_search_inputs(self):
        inputs = get_search_inputs()
        for field in search_field_aliases:
            full = search_field_full_name(inputs, field)
            self.assertIsNotNone(full)
            self.assertIn(full, inputs)

    def test_get_results(self):
        fields = get_search_inputs()
        key = search_field_full_name(fields.keys(), 'email')
        fields[key] = 'dry@middlebury.edu'

        result = get_results(fields)[0]
        self.assertEqual(result.email, 'dry@middlebury.edu')
        self.assertEqual(result.name, 'Dry, Murray P.')
        self.assertEqual(result.webid, '076325FE8E9D69193C080B0052AB9561')

    def test_get_person(self):
        webid = '076325FE8E9D69193C080B0052AB9561'
        person = get_person(webid)

        self.assertEqual(person.email, 'dry@middlebury.edu')
        self.assertEqual(person.name, 'Dry, Murray P.')


class SearchTests(TestCase):
    def test_set_query_init(self):
        q = Search('make the directory great again')
        self.assertEqual(q.query, 'make the directory great again')

    def test_set_query_setter(self):
        q = Search()
        q.query = 'make the directory great again'
        self.assertEqual(q.query, 'make the directory great again')

    def test_set_advanced_search(self):
        q = Search(email='email@middlebury.edu')
        self.assertEqual(q.email, 'email@middlebury.edu')

    def test_validate(self):
        valid_dept = Search(department='Computer Science')
        valid_dept.validate()

        invalid_dept = Search(department='Not A Department')
        with self.assertRaises(DirectoryValidationException):
            invalid_dept.validate()

        valid_field = Search(address='MBH 200')
        valid_field.validate()

        # Need to set invalid field with set attr since
        # keyword args are restricted to known fields
        invalid_field = Search()
        invalid_field.room = 'MBH 200'
        with self.assertRaises(DirectoryValidationException):
            invalid_field.validate()

        valid_person_type = Search(person_type='Student')
        valid_person_type.validate()

        invalid_person_type = Search(person_type='Not A Type')
        with self.assertRaises(DirectoryValidationException):
            invalid_person_type.validate()

        simple_advanced = Search()
        simple_advanced.query = 'test'
        simple_advanced.email = 'test@test.com'
        with self.assertRaises(DirectoryValidationException):
            simple_advanced.validate()

    def test_search(self):
        query = Search(email='dry@middlebury.edu')
        results = query.results()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].webid, '076325FE8E9D69193C080B0052AB9561')

    def test_simple_search(self):
        query = Search('murray dry')
        results = query.results()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].webid, '076325FE8E9D69193C080B0052AB9561')


class SearchMethodTests(TestCase):
    def test_search_method(self):
        results = search(email='dry@middlebury.edu')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].webid, '076325FE8E9D69193C080B0052AB9561')

    def test_search_method_simple_search(self):
        results = search('murray dry')

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].webid, '076325FE8E9D69193C080B0052AB9561')
