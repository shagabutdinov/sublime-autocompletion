Sublime autocompletion plugin.
==============================

Sublime autocompletion plugin with Vim-like autocompletion behaviour.


Features
--------

- Final completion-list - when you got to the last or first completion it stacks at last/first completion (no cycling)

- Obvious completion-list - unlike default sublime word match, it search forward/backward through current file from current cursor position and order matches with first backward/forward occurence

- Start word is completion also - you can return back to initial word with navigation through completion list

- Any part of word completion start - change current word with completioning it from any part (example completion list for o|rder: [ occurence, order, ... ] )


Configuration
-------------

This is my preferred completion configuration. Add it to your ".sublime-keymap" to start using the plugin.

    $ { "keys": ["ctrl+]"], "command": "anyword_completion", "context":
    $   [
    $     { "key": "num_selections", "operator": "equal", "operand": 1 },
    $     { "key": "overlay_visible", "operator": "equal", "operand": false },
    $     { "key": "panel_visible", "operator": "equal", "operand": false }
    $   ]
    $ },
    $ { "keys": ["ctrl+["], "command": "anyword_completion", "args": { "direction": "desc" }, "context":
    $   [
    $     { "key": "num_selections", "operator": "equal", "operand": 1 },
    $     { "key": "overlay_visible", "operator": "equal", "operand": false },
    $     { "key": "panel_visible", "operator": "equal", "operand": false }
    $   ]
    $ }


TODO
----

I'm going to add completion list building with all opened files (not only current).