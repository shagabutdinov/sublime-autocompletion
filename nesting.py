import sublime

try:
  from Expression import expression
  from Autocompletion import utility
  from Autocompletion.word import _set_fuzzy_expression
except ImportError as error:
  sublime.error_message("Dependency import failed; please read readme for " +
   "Autocompletion plugin for installation instructions; to disable this " +
   "message remove this plugin; message: " + str(error))
  raise error

import re

WORD = r'\$?[\w\-]+$' # r'[$\w\.\\/]+((::|->)[$\w\.\\/\-]+)*$'
SEARCH = r'(?:\W|^)(__WORD__[$\w\.\\/]*((::|->|-)[$\w\.\\/]+)*)'

def create_completion(view, backward, word = WORD, search = SEARCH):
  completions = utility.initiate_completions(view, word)
  completions, words, word = completions
  if word == None:
    return None

  text = view.substr(sublime.Region(0, view.size()))
  search = search.replace('__WORD__', word)


  return _find_completions(view, backward, completions, words, word, search)

FUZZY_WORD = WORD
FUZZY_DELIMETER = r'([\w\-\.$\\]|::|->)*'
FUZZY_LAST_DELIMETER = FUZZY_DELIMETER + r'\w'
FUZZY_SEARCH = r'(?:[^\w$]|^)([_\\]*__FUZZY__)'

def create_fuzzy_completion(view, backward, word = FUZZY_WORD,
  delimeter = FUZZY_DELIMETER, last_delimeter = FUZZY_LAST_DELIMETER,
  search = FUZZY_SEARCH):

  completions, words, word = utility.initiate_completions(view, word)
  if word == None:
    return None

  text, point_range, shift = utility.get_text(view, backward)

  search = _set_fuzzy_expression(search, word, delimeter, last_delimeter)

  return _find_completions(view, backward, completions, words, word, search)

def _find_completions(view, backward, completions, words, word, search):
  lookup_arguments = True
  for sel in view.sel():
    if expression.get_nesting(view, sel.b, 1024 * 5) == None:
      lookup_arguments = False
      break

  point = view.sel()[0].b
  cursor = None
  if backward:
    point -= len(word)
    cursor = 'end'

  matches = expression.find_matches(view, point, search, {'backward': backward,
    'nesting': True, 'string': True, 'cursor': cursor,})

  for match in matches:
    start = match.start(1)

    call_end = _get_call_end(view, match)
    if call_end != None:
      _append_region(view, completions, words, sublime.Region(start, call_end))

    if lookup_arguments:
      arg_end = _get_argument_end(view, match)
      if arg_end != None:
        _append_region(view, completions, words, sublime.Region(start, arg_end))

  return completions

def _get_argument_end(view, match):
  nesting = expression.get_nesting(view, match.start(1) + 1, 1024 * 5)
  if nesting == None:
    return None

  return nesting[1]

def _get_call_end(view, match):
  _, point, _, _ = expression.lookup(view, match.end(1), r'^\s*([\(\[])',
    {'nesting': True, 'range': [0, 52], 'limit': 1})

  if point == None:
    return

  nesting = expression.get_nesting(view, point + 1, [1, 1024 * 5])
  if nesting == None:
    return None

  return nesting[1] + 1

def _append_region(view, completions, words, region):
  complete = view.substr(region)
  completion = utility.get_completion(completions, words, complete)
  utility.append_region(completion, [0, view.size()], 0, region.a, region.b)