/* Test cases of folding */

// folds anonymous functions
var Anonymous = function (a, b, c) {
    // bye
};

// folds named functions
function named(a, b, c) {
    // bye
}

// folds constructors with object literals (with "fold_constructors": true)
var constructed = new Anonymous({
    a: "bye",
    b: "bye",
    c: outer = function () {
        var i = 0;
        var nested = function () {
            // bye
        };
        var inner = function () {
            // bye
        };

        // should not fold conditionals or for loops
        if (nested()) {
            return;
        }
        for (i = 0; i < 10; ++i) {
            console.log("bye");
        }
    }
});

// should not fold where your cursor is, even in nested functions
var outer = function () {
    var i = 0;
    var nested = function () {
        // bye
    };
    var inner = function () {
        // bye
    };

    // should not fold conditionals or for loops
    if (nested()) {
        return;
    }
    for (i = 0; i < 10; ++i) {
        console.log("bye");
    }
};