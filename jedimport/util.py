import logging
import os
from pprint import PrettyPrinter

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def chunks(l, n):
  for i in range(0, len(l), n):
    yield l[i:i + n]


def _wrapper(fn, conn, arg):
  os.nice(1)
  try:
    r = fn(arg)
    conn.send(r)
  except Exception as e:
    log.error(e)
    conn.send(None)
  finally:
    conn.close()


def isolated(fn, arg, mp_ctx):

  def wrapped():
    parent_conn, child_conn = mp_ctx.Pipe()
    p = mp_ctx.Process(target=_wrapper, args=(fn, child_conn, arg), daemon=True)
    p.start()
    r = parent_conn.recv()
    p.join()
    return r

  return wrapped
