import logging
import multiprocessing
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from pprint import PrettyPrinter

from jedimport import modules, packages, util
from jedimport.namedb import TrieNameDB

# from pudb import set_trace

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def _all_names():
  mods = sum((p.full_modules() for p in packages.deep_scan()), [])
  mp_ctx = multiprocessing.get_context('spawn')
  cpu_count = multiprocessing.cpu_count()
  with ThreadPoolExecutor(max_workers=cpu_count) as executor:
    futs = [
        executor.submit(util.isolated(modules.scan, chunk, mp_ctx))
        for chunk in util.chunks(mods, 50)
    ]
    return chain.from_iterable(
        chunk for chunk in (f.result() for f in futures.as_completed(futs)))


def build_db():
  return TrieNameDB(
      chain.from_iterable(((v, m[0]) for v in m[1]) for m in _all_names()))
