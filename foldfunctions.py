import sublime, sublime_plugin

settings = {}

def init_plugin():
    global settings

    # Setup settings
    settings = sublime.load_settings('foldfunctions.sublime-settings')

    # I guess these reload on settings change?
    settings.clear_on_change('reload')
    settings.add_on_change('reload', init_plugin)

def plugin_loaded():
    init_plugin()

class CursorListener(sublime_plugin.EventListener):
    # this listener checks if a folded region has been selected
    openBraces = []
    closedBraces = []
    def on_selection_modified_async(self, view):
        unfold = bool(settings.get("select_to_unfold", False))
        syntax = view.settings().get('syntax');
        # syntax should be Packages/JavaScript/JavaScript.sublime-syntax
        if (not unfold or not ("JavaScript" in syntax)):
            return

        # print("cursor", view.sel()[0])
        # braces = view.find_by_selector('meta.brace.curly.js')
        braces = view.find_by_selector('punctuation.definition.block.js')
        hasUnfolded = False
        
        self.openBraces = []
        self.closedBraces = []

        for brace in braces:
            braceStr = view.substr(brace)
            if (braceStr == "{"):
                self.openBraces.append(brace.a)
            elif braceStr == "}":
                region = sublime.Region(self.openBraces.pop(), brace.b)
                self.closedBraces.append(region)

        for brace in self.closedBraces:
            inner = sublime.Region(brace.a + 1, brace.b - 1);
            hasCursor = view.sel()[0].contains(inner)
            if hasCursor and not hasUnfolded:
                hasUnfolded = True
                view.unfold(sublime.Region(brace.a + 1, brace.b - 1))
                return


class FoldFunctionsCommand(sublime_plugin.TextCommand):
    openBraces = []
    closedBraces = []
    def run(self, edit):
        view = self.view
        # braces = view.find_by_selector('meta.brace.curly.js')
        braces = view.find_by_selector('punctuation.definition.block.js')
        parameters = view.find_by_selector('punctuation.definition.parameters.end.js')
        constructors = view.find_by_selector('variable.function.constructor.js')
        self.openBraces = []
        self.closedBraces = []

        closeConstructors = bool(settings.get("fold_constructors", False))

        # unfortunately sublime text doesn't have selectors for starting and closing braces
        # gonna have to search for the opening and closing braces myself
        for brace in braces:
            braceStr = view.substr(brace)
            if (braceStr == "{"):
                self.openBraces.append(brace.a)
            elif braceStr == "}":
                region = sublime.Region(self.openBraces.pop(), brace.b)
                self.closedBraces.append(region)

        for brace in self.closedBraces:
            # check if the brace regions are suitable for closing
            # look at the characters left of the opening brace
            left = sublime.Region(brace.a - 2, brace.a + 1)
            leftStr = view.substr(left)
            leftNoSpac = sublime.Region(brace.a - 1, brace.a + 1)
            leftNoSpacStr = view.substr(leftNoSpac)
            # the cursor should not be here
            sels = self.view.sel()
            hasCursor = False
            for sel in sels:
                hasCursor = hasCursor or brace.intersects(sel);
            # left of brace.a should be parameter list
            hasParameters = False
            for param in parameters:
                if left.intersects(param):
                    hasParameters = True
                    break
            # also close constructors...?
            hasConstructor = False
            if closeConstructors:
                for constructor in constructors:
                    if left.intersects(constructor):
                        hasConstructor = True
                        break
            if (not hasCursor):
                # there might or might not be a space -> function () {} vs function (){}
                if ((leftStr == ") {" and hasParameters) or (leftNoSpacStr == "){" and hasParameters) or hasConstructor):
                    inner = sublime.Region(brace.a + 1, brace.b - 1);
                    view.fold(inner)
