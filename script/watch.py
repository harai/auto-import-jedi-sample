import logging
import re
import subprocess
import sys
from pprint import PrettyPrinter

from isort import SortImports
from yapf.yapflib.yapf_api import FormatFile

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)

python_re = re.compile(r'\.py$')


def is_python(path):
  return bool(re.search(python_re, path))


def updated_paths():
  for line in sys.stdin:
    print(line)
    vals = line.rstrip().split(' ')
    if len(vals) == 3:
      dir, _, file = vals
      yield dir + file
    elif len(vals) == 2:
      file, _ = vals
      yield file
    else:
      print('Unknown notification format:')
      print(line)


def beautify_with_yapf(path):
  _, _, changed = FormatFile(path, in_place=True, style_config='setup.cfg')
  return changed


def get_file_contents(path):
  with open(path, 'r', encoding='utf8') as f:
    return f.read()


def put_file_contents(path, contents):
  with open(path, 'w', encoding='utf8') as f:
    f.write(contents)


def beautify_with_isort(path):
  contents = get_file_contents(path)
  isorted_contents = SortImports(file_contents=contents).output

  if contents == isorted_contents:
    return False
  put_file_contents(path, isorted_contents)
  return True


for path in updated_paths():
  if is_python(path):
    changed = beautify_with_yapf(path)
    if changed:
      continue
    changed = beautify_with_isort(path)
    if changed:
      continue
    subprocess.call(['python', '-m', 'unittest'])
