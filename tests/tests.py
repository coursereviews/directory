from unittest import TestCase

from directory.models import Person
from directory.scraper import get_search_inputs
from directory.helpers import (search_field_aliases,
                               search_field_full_name,
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

def HelperTests(TestCase):
    def test_search_field_full_name(self):
        fields = {'ctl00$ctl00$PageContent$PageContent$middDirectoryForm$txtTelephonenumber': ''}
        full = search_field_full_name(fields.keys(), 'Telephonenumber')

        self.assertIn(full, fields)

class ScraperTests(TestCase):
    def test_get_search_inputs(self):
        inputs = get_search_inputs()
        for field in search_field_aliases:
            full = search_field_full_name(inputs, field)
            self.assertIsNotNone(full)
            self.assertIn(full, inputs)

    def test_valid_person_type(self):
        invalid = 'notaperson'
        self.assertFalse(valid_person_type(invalid))

        valid = 'Student'
        self.assertTrue(valid_person_type(valid))

        valid_aliased = 'Summer Graduate'
        self.assertTrue(valid_person_type(valid_aliased))
