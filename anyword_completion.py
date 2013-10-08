import sublime
import sublime_plugin
import anyword_completion_helper

class AnywordCompletionCommand( sublime_plugin.TextCommand ):

  def run( self, edit, direction = 'asc' ):
    if not hasattr( self, 'completion_helper' ):
      self.completion_helper = anyword_completion_helper.AnywordCompletion()
      self.completion_state = self.completion_helper.create_empty_state()

    self.edit = edit

    cursor_position = self.view.sel()[0].b
    window = self.view.window()

    texts = []
    for view_index, view in enumerate( window.views() ):
      texts.append( view.substr( sublime.Region( 0, view.size() ) ) )

    text_index = window.get_view_index( window.active_view() )[1]

    desc = direction == 'desc'
    self.insert_or_update_completion( cursor_position, texts, text_index,
      desc )

  def insert_or_update_completion( self, cursor_position, texts, text_index, desc ):
    completion = self.completion_helper.get_completion( texts, text_index,
      cursor_position, desc, self.completion_state )

    self.completion_state = completion['state']

    if completion['completion'] is None:
      return None

    edit = self.view.begin_edit()

    self.view.erase( edit, sublime.Region( completion['change_start_position'],
      completion['change_end_position'] ) )

    self.view.insert( edit, completion['change_start_position'],
      completion['completion'] )

    self.view.end_edit( edit )