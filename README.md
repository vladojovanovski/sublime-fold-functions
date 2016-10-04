# Fold Javascript Functions 

A plugin for Sublime Text 3 for Javascript code. This plugin folds all anonymous functions except where your cursor is. This effectively removes all out-of-scope contexts, reducing a lot of noise while programming in JavaScript. 
Default shortcut key is ``cmd+alt+k``. (``ctrl+alt+k`` on Windows) 

![Example gif](/image/example.gif?raw=true "Fold all functions out of scope.")

## Additional features

One thing that annoys me in Sublime Text is to press that tiny triangle to unfold code. An additional feature is added that opens unfolded code by double clicking (selecting) the folded part. If there's any problems or slowdowns with this, you can turn it off in the setttings.

The plugin will also fold object literal parameters inside constructors. This can be turned off in the settings if unwanted.