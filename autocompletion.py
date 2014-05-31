import re

class Autocompletion():

  def get_completion(self, texts, current_text_index, current_cursor_position,
      direction_desc = False, state = None):
    word = self._get_word_for_completion(texts[current_text_index],
      current_cursor_position)

    reset_state = (state is None or 'completion_last' not in state or
      state['completion_last'] != word)

    if reset_state:
      state = self._get_completion_state(texts, current_text_index,
        current_cursor_position, direction_desc)

    if direction_desc:
      state['completion_position'] -= 1
    else:
      state['completion_position'] += 1

    if state['completion_position'] < 0:
      state['completion_position'] = 0

    if state['completion_position'] >= len(state['completions']):
      state['completion_position'] = len(state['completions']) - 1

    completion = state['completions'][state['completion_position']]
    state['completion_last'] = completion

    position_start = self._get_completion_insert_position(
      texts[current_text_index], current_cursor_position)
    word_under_cursor = self._get_word_under_cursor(
      texts[current_text_index], current_cursor_position)
    position_end = None

    if position_start is not None and word_under_cursor is not None:
      position_end = position_start + len(word_under_cursor)

    return {
      'state': state,
      'completion': completion,
      'change_start_position': position_start,
      'change_end_position': position_end
    }

  def create_empty_state(self):
    return self._get_completion_state([''], 0, 0)

  def _get_completion_state(self, texts, current_text_index,
      current_cursor_position, direction_desc = False):
    word = self._get_word_for_completion(texts[current_text_index],
      current_cursor_position)
    word_under_cursor = self._get_word_under_cursor(texts[current_text_index],
      current_cursor_position)

    completions_desc = self._get_completion_list(texts, current_text_index,
      current_cursor_position, True) or []
    completions_asc = self._get_completion_list(texts, current_text_index,
      current_cursor_position, False) or []

    return {
      'current_cursor_position': current_cursor_position,
      'word': word,
      'completions': completions_desc + [word_under_cursor] + completions_asc,
      'completion_position': len(completions_desc)
    }

  def _get_completion_list(self, texts, current_text_index,
      current_cursor_position, direction_desc = False):
    text = texts[current_text_index]
    word = self._get_word_for_completion(text, current_cursor_position)
    if word is None:
      return None

    text_prepared = self._get_text_prepared_for_completion_extraction(texts,
      current_text_index, current_cursor_position, direction_desc)

    return self._get_completion_list_by_word(text_prepared, word,
      direction_desc)

  def _get_text_prepared_for_completion_extraction(self, texts,
      current_text_index, current_cursor_position, direction_desc = False):
    if direction_desc:
      cursor_position = len(' '.join(texts[: current_text_index + 1])) + \
      current_cursor_position - len(texts[current_text_index])
      result = ' '.join(texts[: current_text_index + 1])[: cursor_position]
    else:
      result = ' '.join(texts[current_text_index :])[current_cursor_position :]

    return result

  def _get_completion_list_by_word(self, text, word, direction_desc = False):
    words = re.findall(r'(?:[^\w\d]|^)(' + re.escape(word) + r'[\w\d]+)', text,
      re.M | re.U)

    if direction_desc:
      words.reverse()

    words = self.__uniq(words)

    if direction_desc:
      words.reverse()

    return words

  def _get_word_for_completion(self, text, current_cursor_position):
    start_position = self._get_completion_insert_position(text,
      current_cursor_position)
    if start_position is None:
      return None

    return text[start_position : current_cursor_position]

  def _get_word_under_cursor(self, text, current_cursor_position):
    start_position = self._get_completion_insert_position(text,
      current_cursor_position)

    if start_position is None:
      return None

    end_position = re_result = re.search(r'\A([\w\d_]+)',
      text[current_cursor_position :], re.M | re.U)

    if end_position is None:
      end_position = current_cursor_position
    else:
      end_position = end_position.end(0) + current_cursor_position

    return text[start_position : end_position]

  def _get_completion_insert_position(self, text, current_cursor_position):
    re_result = re.search(r'([\w\d_]+)\Z', text[: current_cursor_position],
      re.M | re.U)

    if re_result is None:
      return None

    return re_result.start(0)

  def __uniq(self, list):
    seen = set()
    return [value for value in list if value not in seen and
      not seen.add(value)]