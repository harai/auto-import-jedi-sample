import logging
from multiprocessing import Pipe, Process
from pprint import PrettyPrinter

from jedimport.namedb import TrieNameDB

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def child_process(conn, values):
  db = TrieNameDB(values)
  while True:
    s = conn.recv()
    if s is None:
      break
    res = db.find_by_prefix(s)
    conn.send(res)

  conn.close()


class ImportsIndexer:

  def __init__(self):
    pass

  def start(self, values):
    self._parent_conn, self._child_conn = Pipe()
    self._p = Process(target=child_process, args=(self._child_conn, values))
    self._p.start()

  def find(self, prefix):
    self._parent_conn.send(prefix)
    return self._parent_conn.recv()

  def join(self):
    self._parent_conn.send(None)
    self._p.join()
