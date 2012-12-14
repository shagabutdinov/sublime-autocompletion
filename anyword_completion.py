import sublime
import sublime_plugin
import anyword_completion_helper

class AnywordCompletionCommand( sublime_plugin.TextCommand ):

  def run( self, edit, direction = 'asc' ):

    # self.view.insert( edit, 0, 'test' )

    if not hasattr( self, 'completion_helper' ):
      self.completion_helper = anyword_completion_helper.AnywordCompletion()
      self.completion_state = self.completion_helper.create_empty_state()

    self.edit = edit

    cursor_position = self.view.sel()[0].b
    text = self.view.substr( sublime.Region( 0, self.view.size() ) )
    desc = direction == 'desc'

    self.insert_or_update_completion( cursor_position, text, desc )

  def insert_or_update_completion( self, cursor_position, text, desc ):
    completion = self.completion_helper.get_completion( [ text ], 0, cursor_position, desc, self.completion_state )
    self.completion_state = completion['state']

    if completion['completion'] is None:
      return None

    edit = self.view.begin_edit()
    # self.view.insert( edit, self.view.size(), "\n\n" + str( self.completion_state ) + "\n\n" )
    self.view.erase( edit, sublime.Region( completion['change_start_position'], completion['change_end_position'] ) )
    self.view.insert( edit, completion['change_start_position'], completion['completion'] )
    self.view.end_edit( edit )