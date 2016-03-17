from unittest import TestCase

from directory.models import Person
from directory.scraper import (get_person,
                               get_search_inputs,
                               get_results)
from directory.helpers import (search_field_aliases,
                               search_field_full_name,
                               valid_department,
                               valid_person_type)


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
