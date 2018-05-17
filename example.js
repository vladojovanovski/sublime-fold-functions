/* Test cases of folding */

// folds anonymous functions
var Anonymous = function (a, b, c) {
    // bye
};

// folds named functions
function named(a, b, c) {
    // bye
}

// folds arrow functions
var arrow = () => { 
    // bye
};

// folds constructors with object literals (with "fold_constructors": true)
var constructed = new Anonymous({
    a: "bye",
    b: "bye",
    c: function () {
        var i = 0;
        var nested = function () {
            // bye
        };
        var inner = function () {
            // bye
        };

        // should not fold conditionals or for loops
        if (nested()) {
            // hi
            return;
        }
        for (i = 0; i < 10; ++i) {
            console.log("hi");
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
        // hi
        return;
    }
    for (i = 0; i < 10; ++i) {
        console.log("hi");
    }
};