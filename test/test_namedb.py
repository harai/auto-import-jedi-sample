import logging
from pprint import PrettyPrinter
from unittest import TestCase

from jedimport.namedb import TrieNameDB

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


class TrieNameDBTest(TestCase):

  def test_find_by_prefix(self):
    data = [
        ('foo', 'FOO'),
        ('bar', 'BAR'),
        ('baz', 'BAZ'),
        ('foofoo', 'FOOFOO'),
        ('foobaz', 'FOOBAZ'),
        ('f', 'F'),
    ]
    db = TrieNameDB(data)

    self.assertEqual(
        set(['FOO', 'FOOBAZ', 'FOOFOO']), set(db.find_by_prefix('foo')))
