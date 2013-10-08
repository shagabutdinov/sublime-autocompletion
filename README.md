Sublime autocompletion plugin.
==============================

Sublime autocompletion plugin with Vim-like autocompletion behaviour.


Features
--------

- Final completion-list - when you got to the last or first completion it stacks at last/first completion (no cycling)

- Obvious completion-list - unlike default sublime word match, it search forward/backward through current file from current cursor position and order matches with first backward/forward occurence

- Start word is completion also - you can return back to initial word with navigation through completion list

- Any part of word completion start - change current word with completioning it from any part (example completion list for o|rder: [ occurence, order, ... ] )

- (upd oct 2013) All opened files are used for build completion list. You can complete word in current file with words of previous/next files. Same rules that listed above are applied for several-files completion.

IMPORTANT NOTICE
----------------

- Tests not cover all features - be careful with pulling and modifying (I used tests because I've never used python before and it was much easier to code with tests than without)

Configuration
-------------

This is my preferred completion configuration. Add it to your ".sublime-keymap" to start using the plugin.

    { "keys": ["ctrl+]"], "command": "anyword_completion", "context":
      [
        { "key": "num_selections", "operator": "equal", "operand": 1 },
        { "key": "overlay_visible", "operator": "equal", "operand": false },
        { "key": "panel_visible", "operator": "equal", "operand": false }
      ]
    },
    { "keys": ["ctrl+["], "command": "anyword_completion", "args": { "direction": "desc" }, "context":
      [
        { "key": "num_selections", "operator": "equal", "operand": 1 },
        { "key": "overlay_visible", "operator": "equal", "operand": false },
        { "key": "panel_visible", "operator": "equal", "operand": false }
      ]
    }


TODO
----

I'm going to add completion list building with all opened files (not only current).