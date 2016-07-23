import abc
import logging
from abc import ABCMeta
from pprint import PrettyPrinter

import msgpack

from marisa_trie import BytesTrie

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def packb_gen(pair_gen):
  for k, v in pair_gen:
    pp.pprint(k)
    pp.pprint(v)
    yield k, msgpack.packb(v)


def unpackb(val):
  return msgpack.unpackb(val)


class NameDB(metaclass=ABCMeta):
  @abc.abstractmethod
  def find_by_prefix(self, str):
    return


class TrieNameDB(NameDB):
  def __init__(self, pair_gen):
    self._data = BytesTrie(packb_gen(pair_gen))

  def find_by_prefix(self, str, limit=10):
    result = []
    count = 0
    for k, v in self._data.itemsiter(str):
      result.append((k, unpackb(v)))
      count += 1
      if count == limit:
        break
    return result
