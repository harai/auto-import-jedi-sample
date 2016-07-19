from pprint import PrettyPrinter

from jedi import Script
from jedi.api.completion import Completion
from jedi.evaluate.helpers import FakeName
from pudb import set_trace

pp = PrettyPrinter(indent=3)

source = ''''''
set_trace()
script = Script(source, 1, 0, 'example.py')
completion = Completion(
    script._evaluator, script._get_module(), script._code_lines,
    script._pos, script.call_signatures
)
completions = completion._trailer_completions(
    FakeName('datetime', script._get_module()))
pp.pprint(completions)
