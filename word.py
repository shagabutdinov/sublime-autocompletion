from Autocompletion import utility
import re

def create_completion(view, backward, word = r'[\w\-]+$',
  search = r'(?:[^\w]|^)(__WORD__[\w\-]*\w)'):

  completions, words, word = utility.initiate_completions(view, word)
  if word == None:
    return None

  text, point_range, shift = utility.get_text(view, backward)

  for match in utility.find_matches(text, backward, search, word):
    completion = utility.get_completion(completions, words, match.group(1))
    utility.append_region(completion, point_range, shift, match.start(1),
      match.end(1))

  return completions

def create_fuzzy_completion(view, backward, word = r'[\w\-]+$',
  delimeter = r'[\w\-]*', last_delimeter = r'[\w\-]*\w',
  search = r'(?:[^\w]|^)([_\\]*__FUZZY__)'):

  completions, words, word = utility.initiate_completions(view, word)
  if word == None:
    return None

  text, point_range, shift = utility.get_text(view, backward)

  search = _set_fuzzy_expression(search, word, delimeter, last_delimeter)

  for match in utility.find_matches(text, backward, search, word):
    completion = utility.get_completion(completions, words, match.group(1))
    utility.append_region(completion, point_range, shift, match.start(1),
      match.end(1))

  return completions

def _set_fuzzy_expression(search, word, delimeter, last_delimeter):
  fuzzy = ''
  for char in word[:-1]:
    fuzzy += re.escape(char) + delimeter

  fuzzy += (r'(' + re.escape(word[-1]) + last_delimeter + '|' +
    re.escape(word[-1]) + r')')

  return search.replace('__FUZZY__', fuzzy)
