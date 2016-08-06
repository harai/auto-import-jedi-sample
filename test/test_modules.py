import logging
from pprint import PrettyPrinter
from unittest import TestCase

from jedimport import modules

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


class ImportsIndexerTest(TestCase):

  def test(self):
    self.assertNotEqual([], modules.scan([['requests', 'utils']]))
