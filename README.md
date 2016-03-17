# Fold Functions 

A plugin for Sublime Text 3 for Javascript code. Folds all anonymous functions and object literal parameters inside constructors, unless your cursor is inside it. Default shortcut key is cmd+alt+k (control on Win). 

## Additional feature

One thing that annoys me in Sublime Text is to press that tiny triangle to unfold code. An additional feature is added that opens unfolded code by double clicking (selecting) the folded part.
(TODO: make this feature optional)

## Requirements

Your JS code should be JSLint-ed or the plugin won't be able to find the functions.

## Example

```
/* A constructor function for Cat */
var Cat = function (specs) {
    this.name = specs.name || "";
    this.age = specs.age || 0;
    this.meow = function () {
        console.log("Meow!");
    };
};

/* Make a new cat */
var cat = new Cat({
    name: "Lucky Kat",
    age: 2
});

cat.meow();

```
After folding (assuming your cursor is outside every function here):

```
/* A constructor function for Cat */
var Cat = function (settings) {[...]};

/* Make a new cat */
var cat = new Cat({[...]});

cat.meow();

```
