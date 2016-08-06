import importlib
from itertools import chain
from pprint import PrettyPrinter

from jedi import Script
from jedi.evaluate import finder
from jedi.evaluate.helpers import FakeName
from jedi.evaluate.imports import Importer

# from pudb import set_trace

pp = PrettyPrinter(indent=3)


def _import_module(module_name):
  paths = module_name
  if 1 < len(paths):
    importlib.import_module('.'.join(paths[0:-1]))


def scan(module_names):
  t = Traverser()
  return list(
      ('.'.join(name), list(str(n) for n in t.names_in_module(name)))
      for name in module_names)


class Traverser:

  def __init__(self):
    self._script = Script('', 1, 0, 'example.py')
    self._module = self._script._get_module()

  def names_in_module(self, module_name):
    try:
      _import_module(module_name)
    except Exception as e:
      pp.pprint(e)
      return []

    imp = Importer(
        self._script._evaluator, [FakeName('.'.join(module_name))],
        self._module, 0)
    try:
      scope_set = imp.follow()
    except Exception as e:
      # print('Error "{}" in {}, ignoring...'.format(e, module_name))
      return []

    all_names = []
    for s in scope_set:
      names = []
      for names_dict in s.names_dicts(search_global=False):
        names += chain.from_iterable(names_dict.values())

      all_names += finder.filter_definition_names(names, self._module)
    return all_names
