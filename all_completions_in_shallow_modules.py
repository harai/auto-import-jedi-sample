from itertools import chain
from pprint import PrettyPrinter

from jedi import Script
from jedi.evaluate import finder
from jedi.evaluate.imports import Importer

# from pudb import set_trace

pp = PrettyPrinter(indent=3)

source = ''''''
# set_trace()
script = Script(source, 1, 0, 'example.py')


def completions_in_module(name, script):
  i = Importer(
      script._evaluator,
      [name],
      script._get_module(),
      0)
  scope_set = i.follow()

  completion_names = []
  for s in scope_set:
    names = []
    for names_dict in s.names_dicts(search_global=False):
      names += chain.from_iterable(names_dict.values())

    completion_names += finder.filter_definition_names(
        names, script._get_module())
  return completion_names

i = Importer(script._evaluator, [], script._get_module(), 0)
vals = i.completion_names(script._evaluator, only_modules=True)

completions = set()
for name in vals:
  completions.update(completions_in_module(name, script))
pp.pprint(len(completions))
