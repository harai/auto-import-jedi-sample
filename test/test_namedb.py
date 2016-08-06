import logging
from pprint import PrettyPrinter
from unittest import TestCase

from jedimport.namedb import TrieNameDB

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


class TrieNameDBTest(TestCase):

  def test_find_by_prefix(self):
    data = [
        ('namedtuple', 'collections'),
        ('OrderedDict', 'collections'),
        ('UserDict', 'collections'),
        ('UserList', 'collections'),
        ('datetime', 'datetime'),
        ('date', 'datetime'),
        ('displayhook', 'sys'),
    ]
    db = TrieNameDB(data)

    self.assertEqual(
        set([('namedtuple', 'collections')]), set(db.find_by_prefix('nam')))
    self.assertEqual(
        set([('OrderedDict', 'collections')]), set(db.find_by_prefix('ord')))
    self.assertEqual(
        set([('UserDict', 'collections'), ('UserList', 'collections')]),
        set(db.find_by_prefix('us')))
    self.assertEqual(
        set(
            [
                ('datetime', 'datetime'), ('date', 'datetime'),
                ('displayhook', 'sys')
            ]), set(db.find_by_prefix('d')))
