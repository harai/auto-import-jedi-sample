from itertools import chain
from pprint import PrettyPrinter

from jedi import Script
from jedi.api.completion import Completion
from jedi.evaluate import finder
from jedi.evaluate.helpers import FakeName
from jedi.evaluate.imports import Importer
from pudb import set_trace

pp = PrettyPrinter(indent=3)

source = ''''''
set_trace()
script = Script(source, 1, 0, 'example.py')
completion = Completion(
    script._evaluator, script._get_module(), script._code_lines, script._pos,
    script.call_signatures)
i = Importer(
    script._evaluator, [FakeName('datetime', script._get_module())],
    script._get_module(), 0)
scope_set = i.follow()

completion_names = []
for s in scope_set:
  names = []
  for names_dict in s.names_dicts(search_global=False):
    names += chain.from_iterable(names_dict.values())

  completion_names += finder.filter_definition_names(
      names, script._get_module())

pp.pprint(completion_names)
