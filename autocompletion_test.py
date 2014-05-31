import unittest
import autocompletion

class AutocompletionTest(unittest.TestCase):

  def setUp(self):
    self.obj = autocompletion.Autocompletion()

  def test_get_word_for_completion(self):
    method = self.obj._get_word_for_completion
    self.assertEqual('test', method('test', 4))
    self.assertEqual('te', method('test', 2))
    self.assertEqual('text', method('test text', 9))
    self.assertEqual('text', method('text test text', 14))
    self.assertEqual('test', method('text test text', 9))
    self.assertEqual('text', method('''test
text
test''', 9))
    self.assertEqual(None, method('test ', 5))

  def test_get_completion_insert_position(self):
    method = self.obj._get_completion_insert_position
    self.assertEqual(0, method('test', 4))
    self.assertEqual(0, method('test text', 4))
    self.assertEqual(5, method('test text', 6))
    self.assertEqual(None, method('test ', 5))

  def test_get_word_under_cursor(self):
    method = self.obj._get_word_under_cursor
    self.assertEqual('test', method('test', 2))
    self.assertEqual('test2', method('test1 test2 test3', 8))


  def test_get_completion_list_by_word(self):
    method = self.obj._get_completion_list_by_word

    self.assertEqual([ 'test' ], method('test', 'te'))
    self.assertEqual([ 'test1', 'test2' ], method('test1 test2', 'te'))
    self.assertEqual([ 'test1', 'test2' ], method('test1 test2 nope', 'te'))

    actual = method('test1 test2 test1 nope', 'te')
    self.assertEqual([ 'test1', 'test2' ], actual)

    self.assertEqual([ 'test1', 'test2' ], method('test test1 test2', 'test'))

  def test_get_text_prepared_for_completion_extraction(self):
    method = self.obj._get_text_prepared_for_completion_extraction
    actual = method([ 'test1', 'test21 test22', 'test3' ], 1, 0)
    self.assertEqual('test21 test22 test3', actual)

    actual = method([ 'test1', 'test21 test22', 'test3' ], 2, 0)
    self.assertEqual('test3', actual)

    actual = method([ 'test1', 'test21 test22', 'test3' ], 1, 7)
    self.assertEqual('test22 test3', actual)

    actual = method([ 'test1', 'test21 test22', 'test3' ], 0, 5, True)
    self.assertEqual('test1', actual)

    actual = method([ 'test1', 'test21 test22', 'test3' ], 1, 0, True)
    self.assertEqual('test1 ', actual)

    actual = method([ 'test1', 'test21 test22', 'test3' ], 2, 0, True)
    self.assertEqual('test1 test21 test22 ', actual)

    actual = method([ 'test1', 'test21 test22', 'test3' ], 1, 6, True)
    self.assertEqual('test1 test21', actual)

  def test_get_completion_list(self):
    method = self.obj._get_completion_list

    actual = method([ 'test1', 'test21 test22', 'te test3' ], 2, 2)
    self.assertEqual([ 'test3' ], actual)

    actual = method([ 'test1', 'test21 test22', 'te test3 test4' ], 2, 2)
    self.assertEqual([ 'test3', 'test4' ], actual)

    actual = method([ 'test1', 'te test21 test22', 'test3' ], 1, 2)
    self.assertEqual([ 'test21', 'test22', 'test3' ], actual)

    actual = method([ 'test1 te', 'test21 test22', 'test3' ], 0, 7, True)
    self.assertEqual([ 'test1' ], actual)

    actual = method([ 'test1', 'test21 te test22', 'test3' ], 1, 9, True)
    self.assertEqual([ 'test1', 'test21' ], actual)

    actual = method([ 'te1 test21 test22 test3 te1 test21 te' ], 0, 42, True)
    self.assertEqual([ 'test22', 'test3', 'te1', 'test21' ], actual)

    self.assertEqual(None, method([ 'test1 ' ], 0, 6, True))

  def test_get_completion_state(self):
    method = self.obj._get_completion_state
    expected = {
      'current_cursor_position': 2,
      'word': 'te',
      'completions': [ 'test1', 'test21', 'test22', 'test', 'test3' ],
      'completion_position': 3
    }

    actual = method([ 'test1', 'test21 test22', 'test test3' ], 2, 2)

    self.assertEqual(expected, actual)

  def test_get_completion(self):
    method = self.obj.get_completion
    actual = method([ 'test1', 'test2', 'te test3' ], 2, 2)
    self.assertTrue('state' in actual)
    self.assertEqual(actual['completion'], 'test3')

    actual = method([ 'te test3 test4 test5' ], 0, 2)
    self.assertEqual('test3', actual['completion'])

    actual = method([ 'test3 test3 test4 test5' ], 0, 5, False, actual['state'])
    self.assertEqual('test4', actual['completion'])

    actual = method([ 'test4 test3 test4 test5' ], 0, 5, False, actual['state'])
    self.assertEqual('test5', actual['completion'])

    actual = method([ 'test5 test3 test4 test5' ], 0, 5, False, actual['state'])
    self.assertEqual('test5', actual['completion'])

    actual = method([ 'test5 test3 test4 test5' ], 0, 5, True, actual['state'])
    self.assertEqual('test4', actual['completion'])

    actual = method([ 'test4 test3 test4 test5' ], 0, 5, True, actual['state'])
    self.assertEqual('test3', actual['completion'])

    actual = method([ 'test3 test3 test4 test5' ], 0, 5, True, actual['state'])
    self.assertEqual('te', actual['completion'])

    actual = method([ 'te test3 test4 test5' ], 0, 5, True, actual['state'])
    self.assertEqual('te', actual['completion'])

  def test_get_completion__with_several_lists(self):
    method = self.obj.get_completion

    actual = method([ 'test1 test2', 'test21 te test3', 'test4 test5' ], 1, 9,
      True)
    self.assertEqual('test21', actual['completion'])

    actual = method([ 'test1 test2', 'test21 test21 test3', 'test4 test5' ], 1,
      13, True, actual['state'])
    self.assertEqual('test2', actual['completion'])

    actual = method([ 'test1 test2', 'test21 test2 test3', 'test4 test5' ], 1,
      12, True, actual['state'])
    self.assertEqual('test1', actual['completion'])

    actual = method([ 'test1 test2', 'test21 test1 test3', 'test4 test5' ], 1,
      12, True, actual['state'])
    self.assertEqual('test1', actual['completion'])

    actual = method([ 'test1 test2', 'test21 test1 test3', 'test4 test5' ], 1,
      12, True, actual['state'])
    self.assertEqual('test1', actual['completion'])

    actual = method([ 'test1 test2', 'test21 test1 test3', 'test4 test5' ], 1,
      12, False, actual['state'])
    self.assertEqual('test2', actual['completion'])

    actual = method([ 'test1 test2', 'test21 test2 test3', 'test4 test5' ], 1,
      12, False, actual['state'])
    self.assertEqual('test21', actual['completion'])

    actual = method([ 'test1 test2', 'test21 test21 test3', 'test4 test5' ], 1,
      13, False, actual['state'])
    self.assertEqual('te', actual['completion'])

    actual = method([ 'test1 test2', 'test21 te test3', 'test4 test5' ], 1, 9,
      False, actual['state'])
    self.assertEqual('test3', actual['completion'])

    actual = method([ 'test1 test2', 'test21 test3 test3', 'test4 test5' ], 1,
      12, False, actual['state'])
    self.assertEqual('test4', actual['completion'])

    actual = method([ 'test1 test2', 'test21 test4 test3', 'test4 test5' ], 1,
      12, False, actual['state'])
    self.assertEqual('test5', actual['completion'])

    actual = method([ 'test1 test2', 'test21 test5 test3', 'test4 test5' ], 1,
      12, False, actual['state'])
    self.assertEqual('test5', actual['completion'])

  def test_get_completion__dropped_when_cursor_moved(self):
    method = self.obj.get_completion

    actual = method([ 'test1 test2', 'test3 te no nope1 test4',
      'test5 test6' ], 1, 8)
    self.assertEqual('test4', actual['completion'])

    actual = method([ 'test1 test2', 'test3 test4 no nope1 nope2 test4',
      'test5 test6' ], 1, 14, False, actual['state'])
    self.assertEqual('nope1', actual['completion'])

  def test_get_completion__works_at_any_part_of_word(self):
    method = self.obj.get_completion

    actual = method([ 'test1' ], 0, 2)
    self.assertEqual('test1', actual['completion'])

    actual = method([ 'test1', 'test2', 'test3', 'test4' ], 0, 2)
    self.assertEqual('test2', actual['completion'])

    actual = method([ 'test2', 'test2', 'test3', 'test4' ], 0, 5, False,
      actual['state'])
    self.assertEqual('test3', actual['completion'])

    actual = method([ 'test3', 'test2', 'test3', 'test4' ], 0, 5, True,
      actual['state'])
    self.assertEqual('test2', actual['completion'])

    actual = method([ 'test2', 'test2', 'test3', 'test4' ], 0, 5, True,
      actual['state'])
    self.assertEqual('test1', actual['completion'])

    actual = method([ 'test1', 'test2', 'test3', 'test4' ], 0, 5, True,
      actual['state'])
    self.assertEqual('test1', actual['completion'])

  def test_get_completion__ranges_is_correct(self):
    method = self.obj.get_completion

    actual = method([ 'test1 test2 test test3 test4' ], 0, 14)
    self.assertEqual('test3', actual['completion'])
    self.assertEqual(12, actual['change_start_position'])
    self.assertEqual(16, actual['change_end_position'])

    actual = method([ 'test1 test2 test3 test3 test4' ], 0, 17, False,
      actual['state'])
    self.assertEqual('test4', actual['completion'])
    self.assertEqual(12, actual['change_start_position'])
    self.assertEqual(17, actual['change_end_position'])

  def test_get_completion__state_should_be_updated_if_word_changes(self):
    method = self.obj.get_completion

    actual = method([ 'test1 test2', 'test21 te test3', 'test4 test5' ], 1, 9,
        True)
    self.assertEqual('test21', actual['completion'])

    actual = method([ 'test1 test2', 'test21 te test3', 'test4 test5' ], 1, 9,
        True, actual['state'])
    self.assertEqual('test21', actual['completion'])

  def test_create_empty_state(self):
    self.obj.create_empty_state()

if __name__ == '__main__':
  unittest.main()