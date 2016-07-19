from pprint import PrettyPrinter

import jedi
from pudb import set_trace

pp = PrettyPrinter(indent=3)

# source = '''import '''
# set_trace()
# script = jedi.Script(source, 1, len('import '), 'example.py')
source = '''
import datetime
datetime.'''
set_trace()
script = jedi.Script(source, 3, len('datetime.'), 'example.py')
completions = script.completions()
print(completions[0].complete)
