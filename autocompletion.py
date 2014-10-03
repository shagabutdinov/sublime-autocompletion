import sublime
import sublime_plugin
import importlib

clean_required = False
_completion = None

def _set_current_completion(completion):
  global _completion
  _completion = completion

def _get_current_completion():
  global _completion
  return _completion

def _call_handler(handler, **args):
  module_name, method_name = handler.rsplit('.', 1)
  module = importlib.import_module(module_name)
  result = getattr(module, method_name)(**args)
  return result

def _create_completion(handler, view, backward, args = {}):
  handler_args = args.copy()
  handler_args.update({
    'backward': backward,
    'view': view
  })

  completions = _call_handler(handler, **handler_args)
  if completions == None:
    return None

  completion = {
    'type': handler + str(args),
    'backward': backward,
    'current': 0,
    'completions': completions,
    'position': view.sel()[0].b - len(completions[0]['completion']),
  }

  return completion

class Autocompletion(sublime_plugin.TextCommand):
  def run(self, edit, handler, backward = True, **args):
    sels = self.view.sel()
    if len(sels) == 0:
      return

    completion = _get_current_completion()
    if self._is_new_completion_needed(handler, completion, backward, args):
      completion = _create_completion(handler, self.view, backward, args)
      if completion == None:
        return
      _set_current_completion(completion)
      self._highlight(completion)

    current_index, current, new = self._get_backward_completion(completion,
      backward)

    for selection in sels:
      self._complete(edit, completion, selection, current_index, current, new,
        backward)

    self._highlight_current(completion)

  def _is_new_completion_needed(self, handler, completion, backward, args):
    if completion == None:
      return True

    if completion['type'] != handler + str(args):
      return True

    _is_completion_valid = self._is_completion_valid(completion,
      self.view.sel()[0], completion['current'], backward)

    if not _is_completion_valid:
      return True

    current = completion['completions'][completion['current']]['completion']
    if self.view.sel()[0].b - len(current) != completion['position']:
      return True

    return False

  def _is_completion_valid(self, completion, selection, index, backward):
    if index == 0:
      if not completion['backward'] and backward:
        return False

      if completion['backward'] and not backward:
        return False

    current = completion['completions'][index]['completion']
    region = sublime.Region(selection.b - len(current), selection.b)
    last = self.view.substr(region)

    return last == current

  def _get_backward_completion(self, completion, backward):
    current_index = completion['current']
    current = completion['completions'][current_index]['completion']

    if completion['backward']:
      backward = not backward

    if backward:
      completion['current'] -= 1
      if completion['current'] < 0:
        completion['current'] = 0
    else:
      completion['current'] += 1
      if completion['current'] > len(completion['completions']) - 1:
        completion['current'] = len(completion['completions']) - 1

    new = completion['completions'][completion['current']]['completion']
    return current_index, current, new

  def _complete(self, edit, completion, selection, index, current, new,
    backward):
    if not self._is_completion_valid(completion, selection, index, backward):
      return

    region = sublime.Region(selection.b - len(current), selection.b)
    self.view.replace(edit, region, new)

  def _highlight(self, completion):
    regions, completions = [], completion['completions']

    global clean_required
    clean_required = True

    for index, current in enumerate(completions):
      if index == 0:
        continue

      highlights = current['highlights']

      self.view.add_regions('autocompletion_' + str(index), highlights)
      if completion['backward']:
        highlights = reversed(highlights)

      regions += highlights
      if len(regions) > 100:
        regions = regions[:100]
        break

    self.view.add_regions('autocompletion', regions, '?', '',
      sublime.DRAW_EMPTY | sublime.DRAW_OUTLINED)

  def _highlight_current(self, completion):
    global clean_required
    clean_required = True

    if completion['current'] == 0:
      self.view.erase_regions('autocompletion_current')
      return

    highlights = self.view.get_regions('autocompletion_' +
      str(completion['current']))

    self.view.add_regions('autocompletion_current', highlights, 'string', '')

class CancelCompletion(sublime_plugin.TextCommand):
  def run(self, edit):
    global completion
    completion = None

class ClearHighlights(sublime_plugin.EventListener):
  def on_selection_modified_async(self, view):
    last_command, _, _ = view.command_history(0)
    if last_command == 'autocompletion':
      return

    global clean_required
    if not clean_required:
      return

    clean_required = False

    view.erase_regions('autocompletion')
    view.erase_regions('autocompletion_current')