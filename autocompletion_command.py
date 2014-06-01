import sublime
import sublime_plugin
import inspect
import Autocompletion

class AutocompletionCommand(sublime_plugin.TextCommand):

  def run(self, edit, regexps = None, direction = 'asc'):
    if not hasattr(self, 'completion_helper'):
      self.completion_helper = Autocompletion.autocompletion.Autocompletion()
      self.completion_state = self.completion_helper.create_empty_state()

    self.edit = edit

    window = self.view.window()

    texts = []
    for view_index, view in enumerate(window.views()):
      texts.append(view.substr(sublime.Region(0, view.size())))

    text_index = window.get_view_index(window.active_view())[1]

    desc = direction == 'desc'
    self.insert_or_update_completion(edit, texts, text_index, regexps, desc)

  def insert_or_update_completion(self, edit, texts, text_index, regexps, desc):
    position = self.view.sel()[0].b

    completion = self.completion_helper.get_completion(texts, text_index,
      position, regexps, desc, self.completion_state)

    self.completion_state = completion['state']

    if completion['completion'] is None:
      return None

    erase_offset = [
      position - completion['change_start_position'],
      completion['change_end_position'] - position
    ]

    global_offset = 0
    first_text = None
    for index, region in enumerate(self.view.sel()):
      edit_start = region.b - erase_offset[0]
      edit_end = region.b + erase_offset[1]

      if index == 0:
        first_text = texts[text_index][edit_start:edit_end]
      elif self.view.substr(sublime.Region(edit_start, edit_end)) != first_text:
        continue

      self.view.erase(edit, sublime.Region(edit_start, edit_end))
      self.view.insert(edit, edit_start, completion['completion'])