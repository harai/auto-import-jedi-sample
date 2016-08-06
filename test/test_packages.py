import logging
from pprint import PrettyPrinter
from unittest import TestCase

from jedimport import packages

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


class ImportsIndexerTest(TestCase):

  def test(self):
    # pp.pprint(list(p.pack() for p in packages.deep_scan()))
    self.assertNotEqual([], packages.deep_scan())
