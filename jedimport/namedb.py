import abc
import collections
import logging
from abc import ABCMeta
from pprint import PrettyPrinter

from marisa_trie import Trie

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


class NameDB(metaclass=ABCMeta):

  @abc.abstractmethod
  def find_by_prefix(self, str):
    return


class TrieNameDB(NameDB):

  def __init__(self, pair_gen):
    self._dic = self._construct_dic(pair_gen)
    self._index = Trie(self._dic.keys())

  def _construct_dic(self, pair_gen):
    dic = collections.defaultdict(list)
    for k, v in pair_gen:
      dic[k.lower()].append((k, v))
    return dic

  def find_by_prefix(self, str, limit=50):
    result = []
    for key in self._index.iterkeys(str.lower()):
      result.extend(self._dic[key])
      if limit <= len(result):
        break
    return result[:limit]
