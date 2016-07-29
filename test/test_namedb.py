import logging
from pprint import PrettyPrinter
from unittest import TestCase

from jedimport.mp import ImportsIndexer

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


class ImportsIndexerTest(TestCase):

  def test_find_by_prefix(self):
    data = [
        ('foo', 'FOO'),
        ('bar', 'BAR'),
        ('baz', 'BAZ'),
        ('foofoo', 'FOOFOO'),
        ('foobaz', 'FOOBAZ'),
        ('f', 'F'),
    ]

    indexer = ImportsIndexer()
    indexer.start(data)

    try:
      self.assertEqual(
          set(['FOO', 'FOOBAZ', 'FOOFOO']), set(indexer.find('foo')))
    finally:
      indexer.join()
