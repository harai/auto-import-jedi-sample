import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from pprint import PrettyPrinter

from jedimport import indexer

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def main():

  with ThreadPoolExecutor(max_workers=1) as executor:
    fut = executor.submit(indexer.build_db)
    for line in sys.stdin:
      line = line.strip()
      if line == 'exit':
        break
      if not fut.done():
        print('Not yet indexed. Wait for a moment...\n')
        print('> ', end='', flush=True)
        continue
      pp.pprint(line)
      pp.pprint(fut.result().find_by_prefix(line.strip()))
      print('> ', end='', flush=True)
