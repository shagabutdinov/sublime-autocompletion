import sublime
import sublime_plugin
import Autocompletion

class AutocompletionCommand(sublime_plugin.TextCommand):

  def run(self, edit, direction = 'asc'):
    if not hasattr(self, 'completion_helper'):
      self.completion_helper = Autocompletion()
      self.completion_state = self.completion_helper.create_empty_state()

    self.edit = edit

    cursor_position = self.view.sel()[0].b
    window = self.view.window()

    texts = []
    for view_index, view in enumerate(window.views()):
      texts.append(view.substr(sublime.Region(0, view.size())))

    text_index = window.get_view_index(window.active_view())[1]

    desc = direction == 'desc'
    self.insert_or_update_completion(edit, cursor_position, texts, text_index,
      desc)

  def insert_or_update_completion(self, edit, cursor_position, texts,
      text_index, desc):
    completion = self.completion_helper.get_completion(texts, text_index,
      cursor_position, desc, self.completion_state)

    self.completion_state = completion['state']

    if completion['completion'] is None:
      return None

    self.view.erase(edit, sublime.Region(completion['change_start_position'],
      completion['change_end_position']))

    self.view.insert(edit, completion['change_start_position'],
      completion['completion'])
