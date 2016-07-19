from pprint import PrettyPrinter

from jedi import Script
from jedi.evaluate.imports import Importer

# from pudb import set_trace

pp = PrettyPrinter(indent=3)

source = ''''''
# set_trace()
script = Script(source, 1, 0, 'example.py')

i = Importer(script._evaluator, [], script._get_module(), 0)
vals = i.completion_names(script._evaluator, only_modules=True)
pp.pprint(vals)
