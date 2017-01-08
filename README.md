# Fold Javascript Functions 

A plugin for Sublime Text 3 for Javascript code. This plugin folds all functions except where your cursor is. This effectively removes all out-of-scope contexts, reducing a lot of noise while programming in JavaScript. 
Default shortcut key is ``cmd+alt+k``. (``ctrl+alt+k`` on Windows) 

![Example gif](https://github.com/LuckyKat/sublime-fold-functions/blob/master/image/example.gif "Fold all functions out of scope.")

## Additional features

* ``select_to_unfold``: (on by default) One thing that annoys me in Sublime Text is to press that tiny triangle to unfold code. With this you can double click (which selects code) to open a folded block.
* ``fold_constructors``: (off by default) The plugin will also fold object literal parameters inside constructors.
* ``auto_fold``: (off by default) An experimental feature. Automatically folds and unfolds while you move your cursor. 

## Requirements

The functions must use 1TBS brace style, if the opening brace is on a new line, the functions won't be recognized.

Make sure you have the latest version of Sublime Text 3 installed. As of writing, build 3126.
The plugin makes use of Sublime's selectors to recognize the blocks with curly braces. Unfortunately, this keeps changing on every now and then (twice now since development of this plugin).

No support for Sublime Text 2, sorry.
