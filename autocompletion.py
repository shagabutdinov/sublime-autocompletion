import re

class Autocompletion():

  def __init__(self):
    self.types = {
      "words": '(?:[^_\w]|^)(__WORD__[\w]+)',
      "subwords": '(?:[^\w]|_|[A-Z]|^)(__WORD__[\w]?)(?:_|[A-Z]|$)',
      "line": '(?:[^\w]|^)(__WORD__.*)',
    }

  def get_completion(self, texts, text_index, position, regexps, desc = False,
    state = None):

    text = texts[text_index]
    insert_positions = self._get_insert_positions(text, position, regexps)
    state, state_resetted = self._get_updated_state(texts, text_index, position,
      regexps, state, desc)

    if state_resetted:
      state['start_position'] = insert_positions[0]

    if state['completion_last']:
      state['last_position'] = state['start_position'] + len(state['completion_last'])

    return {
      'state': state,
      'completion': state['completion_last'],
      'change_start_position': state['start_position'],
      'change_end_position': position,
    }

  def _get_regexps(self, regexps):
    if regexps == None:
      result = {
        'search': '(?:[^_\w]|^)(__WORD__[\w]+)',
      }
    elif type(regexps) is dict:
      result = regexps
    else:
      result = {
        'search': regexps,
      }

    if not ('word' in result):
      result['word'] = '([\w]+)\Z'

    return result

  def create_empty_state(self):
    return self._get_completion_state([''], 0, 0, None, 'asc')

  def _get_updated_state(self, texts, text_index, position, regexps, state,
      desc):

    text = texts[text_index]
    last_position = 'last_position' in state and state['last_position']
    last_completion = 'completion_last' in state and state['completion_last']

    current = None
    if last_position and last_completion:
      current = text[last_position - len(last_completion):last_position]

    reset_state = (
      state is None or
      'last_regexps' not in state or
      state['last_regexps'] != regexps or
      last_position != position or
      current != last_completion
    )

    if reset_state:
      state = self._get_completion_state(texts, text_index, position, regexps,
        desc)

    state['last_regexps'] = regexps

    if desc:
      state['completion_position'] -= 1
    else:
      state['completion_position'] += 1

    if state['completion_position'] < 0:
      state['completion_position'] = 0

    if state['completion_position'] >= len(state['completions']):
      state['completion_position'] = len(state['completions']) - 1

    completion = state['completions'][state['completion_position']]
    state['completion_last'] = completion

    return [state, reset_state]

  def _get_completion_state(self, texts, text_index, position, regexps, desc):
    word = self._get_word(texts[text_index], position, regexps)

    completions_desc, completions_asc = [], []

    if word:
      completions_desc = self._get_completion_list(texts, text_index, position,
        word, regexps, True)
      completions_asc = self._get_completion_list(texts, text_index, position,
        word, regexps, False)

    return {
      'position': position,
      'word': word,
      'completions': completions_desc + [word] + completions_asc,
      'completion_position': len(completions_desc)
    }

  def _get_completion_list(self, texts, text_index, position, word, regexps, desc):
    text = self._get_joined_text(texts, text_index, position, desc)
    return self._get_completion_list_by_word(text, word, regexps, desc)

  def _get_joined_text(self, texts, text_index, position, desc = False):
    if desc:
      cursor_position = len(' '.join(texts[: text_index + 1])) + \
      position - len(texts[text_index])
      result = ' '.join(texts[: text_index + 1])[: cursor_position]
    else:
      result = ' '.join(texts[text_index :])[position :]

    return result

  def _get_completion_list_by_word(self, text, word, regexps, desc = False):
    regexp_string = self._get_regexps(regexps)['search'].\
      replace('__WORD__', word)

    regexp = re.compile(regexp_string)
    words = re.findall(regexp, text)

    if desc:
      words.reverse()

    words = self.__uniq(words)

    if desc:
      words.reverse()

    return words

  def _get_word(self, text, position, regexps):
    start_position = self._get_completion_insert_position(text, position,
      regexps)

    if start_position is None:
      return None

    return text[start_position:position]

  def _get_completion_insert_position(self, text, position, regexps):
    regexp = re.compile(self._get_regexps(regexps)['word'])
    re_result = re.search(regexp, text[:position])

    if re_result is None:
      return None

    return re_result.start(0)

  def _get_insert_positions(self, text, position, regexps):
    position_start = self._get_completion_insert_position(text, position,
      regexps)

    word_under_cursor = self._get_word(text, position, regexps)

    return [position_start, position]

  def __uniq(self, list):
    seen = set()
    return [value for value in list if value not in seen and
      not seen.add(value)]