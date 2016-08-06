import logging
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor
from pprint import PrettyPrinter
from unittest import TestCase

from jedimport import util

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def show(res, arg):
  pp.pprint('res: {}, arg: {}'.format(res, arg))


def task(arg):
  return arg * 2


class IsolatedTest(TestCase):

  def test(self):
    mp_ctx = multiprocessing.get_context('spawn')
    with ThreadPoolExecutor(max_workers=2) as executor:
      futs = [
          executor.submit(util.isolated(task, i, mp_ctx)) for i in range(10)
      ]
      time.sleep(2)
      self.assertTrue(all(f.done() for f in futs))
      self.assertTrue(all(f.result() % 2 == 0 for f in futs))
