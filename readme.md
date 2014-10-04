# Sublime Autocompletion plugin

This is really glorious plugin that reduce plain typing considerably while
coding.


### Demo

![Demo](https://raw.github.com/shagabutdinov/sublime-autocompletion/master/demo/demo.gif "Demo")


### Features

Provides 8 different types of autocompletion:

1. Complete word - basic completion; completes word that occurenced in text and
opened files.

2. Complete word (fuzzy) - like "complete word" but uses fuzzy match over words.

3. Complete subword - completes snake_case and CamelCase words parts.

4. Complete long word - complete long words: class names with namespaces
(Class::Name), method calls (object.method), filenames (file/name.py), urls
(http://...).

5. Complete long word (fuzzy) - line "complete long word" but uses fuzzy match
over words.

6. Complete nesting - completes over and into brackets: can complete full method
call (method(arg1, arg2)), method arguments (arg1, arg2), array ([value1,
value2]) and everything that has brackets over it or after it.

7. Complete nesting (fuzzy) - like "complete nesting" but uses fuzzy match.

8. Complete line - competes whole line.

However it maps only 6 types of autocompletion. Not fuzzy completions aren't
mapped to keyboard shortcuts by default. See "installation" section if you would
like map non-fuzzy completion behavior.

All lists are build in order of first occurence of word. That makes autocomplete
very predictable and easy to use.

Words completion works over all files opened. Nesting completion works only in
current file (because of performance issues)


### Installation

This plugin is part of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
plugin set. You can install sublime-enhanced and this plugin will be installed
automatically.

If you would like to install this package separately check "Installing packages
separately" section of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
package.

If you don't like fuzzy behavior you should rebind keyboard shortcuts after
installation in the "Autocompletion/Default (OSNAME).sublime-keymap" file
(non-fuzzy behavior are commented by default).


### Usage

Type a one of two characters of the beginning of word. Than hit keyboard
shortcut or run command to complete the word. You can run same command again to
complete next/previous occurence.

If you like fuzzy completion it is really useful to type a start character and
following character from the middle of word to receive more accurate completion.
E.g. for complete local_variable type "lv" and hit keyboard shortcut. First
character of word should always be character of completion. However if word
starts with underscore (_) it possible to type next character, e.g. for complete
_local_variable same "lv" will work.


### Commands

| Description                         | Keyboard shortcuts | Command palette                                        |
|-------------------------------------|--------------------|--------------------------------------------------------|
| Complete word forward (fuzzy)       | ctrl+p             | Autocompletion: complete word forward (fuzzy)          |
| Complete word backward (fuzzy)      | ctrl+o             | Autocompletion: complete word backward (fuzzy)         |
| Complete word forward               |                    | Autocompletion: complete word forward                  |
| Complete word backward              |                    | Autocompletion: complete word backward                 |
| Complete subword forward            | ctrl+shift+p       | Autocompletion: complete subword forward               |
| Complete subword backward           | ctrl+shift+o       | Autocompletion: complete word backward                 |
| Complete long word forward (fuzzy)  | ctrl+alt+p         | Autocompletion: complete long word forward (fuzzy)     |
| Complete long word backward (fuzzy) | ctrl+alt+o         | Autocompletion: complete long word backward (fuzzy)    |
| Complete long word forward          |                    | Autocompletion: complete long word forward             |
| Complete long word backward         |                    | Autocompletion: complete long word backward            |
| Complete nesting forward (fuzzy)    | alt+p              | Autocompletion: complete nesting forward (fuzzy)       |
| Complete nesting backward (fuzzy)   | alt+o              | Autocompletion: complete nesting backward (fuzzy)      |
| Complete nesting forward            |                    | Autocompletion: complete nesting forward               |
| Complete nesting backward           |                    | Autocompletion: complete nesting backward              |
| Complete line forward               | alt+shift+p        | Autocompletion: complete line forward                  |
| Complete line backward              | alt+shift+o        | Autocompletion: complete line backward                  |


### Dependencies

https://github.com/shagabutdinov/sublime-expression
