import sublime
import re

def get_word_info(view, expression):
  line_region = view.line(view.sel()[0].b)
  previous = view.substr(sublime.Region(line_region.begin(), view.sel()[0].b))
  word_match = re.search(expression, previous)
  if word_match == None:
    return None, []

  word = word_match.group(0)
  word_region = sublime.Region(
    line_region.begin() + word_match.start(0),
    line_region.begin() + word_match.end(0)
  )

  return word, [word_region]

def initiate_completions(view, expression):
  word, word_region = get_word_info(view, expression)
  completions = [{'completion': word, 'highlights': word_region}]
  return completions, [word], word

def get_completion(completions, words, word):
  if word in words:
    completion = completions[words.index(word)]
  else:
    completion = {'completion': word, 'highlights': []}
    completions.append(completion)
    words.append(word)

  return completion

def append_region(completion, point_range, shift, start, end):
  if point_range[0] <= start and end <= point_range[1]:
    region = sublime.Region(start + shift, end + shift)
    completion['highlights'].append(region)

def find_matches(text, backward, search, word):
  search = search.replace('__WORD__', re.escape(word))
  matches = re.finditer(search, text)

  if backward:
    matches = reversed(list(matches))

  return matches

def get_text(view, backward):
  point = view.sel()[0].b

  if backward:
    region = sublime.Region(0, point)
  else:
    region = sublime.Region(point, view.size())

  text = view.substr(region)

  if backward:
    views = sublime.active_window().views()
  else:
    views = reversed(sublime.active_window().views())

  size = 0
  texts = []
  for current_view in views:
    if current_view.id() == view.id():
      break

    current_text = current_view.substr(sublime.Region(0, current_view.size()))
    size += len(current_text) + 1
    texts.append(current_text)

  if len(texts) > 0:
    if backward:
      text = "\n".join(texts) + "\n" + text
    else:
      text = text + "\n" + "\n".join(reversed(texts))

  start, end = region.a, region.b
  if backward:
    start += size
    end += size
  else:
    start -= point
    end -= point

  if backward:
    shift = 0
  else:
    shift = point

  return text, [start, end], shift - start