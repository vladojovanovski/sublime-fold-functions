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
    def on_selection_modified_async(self, view):
        unfold = bool(settings.get("select_to_unfold", False))
        syntax = view.settings().get('syntax');
        responsiveMode = bool(settings.get("auto_fold", False))
        # syntax should be Packages/JavaScript/JavaScript.sublime-syntax
        if (not unfold or not ("JavaScript" in syntax)):
            return

        # print("cursor", view.sel()[0])
        hasUnfolded = False

        # undocumented function :|
        foldedRegions = view.folded_regions()

        sels = view.sel()
        if responsiveMode:
            # unfold by passing cursor then fold everything
            for region in foldedRegions:
                outer = sublime.Region(region.a - 1, region.b + 1);
                hasCursor = False
                for sel in sels:
                    if sel.intersects(outer):
                        view.unfold(region)
            # 2 is for making the selection a little larger
            fold(view, 2)
        else:
            # unfold by double clicking
            for region in foldedRegions:
                inner = sublime.Region(region.a + 1, region.b - 1);
                hasCursor = view.sel()[0].contains(inner)
                if hasCursor and not hasUnfolded:
                    hasUnfolded = True
                    view.unfold(region)
                    return

def collectBraces (view):
    braces = view.find_by_selector('meta.brace.curly.js') + view.find_by_selector('punctuation.definition.block.js')
    openBraces = []
    closedBraces = []
    # unfortunately sublime text doesn't have selectors for starting and closing braces
    # gonna have to search for the opening and closing braces myself
    # TODO: since build 1326 or so there is meta.block.js
    # edit 2016/6/11: or not.... view.find_by_selector only returns outer regions, still need to look into this
    for brace in braces:
        braceStr = view.substr(brace)
        if (braceStr == "{"):
            openBraces.append(brace.a)
        elif braceStr == "}":
            region = sublime.Region(openBraces.pop(), brace.b)
            closedBraces.append(region)

    return closedBraces

def fold (view, edge):
    regions = collectBraces(view)

    parameters = view.find_by_selector('punctuation.definition.parameters.end.js')
    closeConstructors = bool(settings.get("fold_constructors", False))
    sels = view.sel()

    for region in regions:
        # check if the brace regions are suitable for closing
        # look at the characters left of the opening brace
        left = sublime.Region(region.a - 2, region.a + 1)
        leftStr = view.substr(left)
        leftNoSpac = sublime.Region(region.a - 1, region.a + 1)
        leftNoSpacStr = view.substr(leftNoSpac)
        # the cursor should not be here
        hasCursor = False
        for sel in sels:
            extraSel = sublime.Region(sel.a - edge, sel.a + edge)
            hasCursor = hasCursor or region.intersects(extraSel);
        # left of region.a should be parameter list
        hasParameters = False
        for param in parameters:
            if left.intersects(param):
                hasParameters = True
                break
        # also close constructors...?
        hasConstructor = False
        if closeConstructors:
            # check if it's an object literal inside a constructor
            # the scope should end with meta.function-call.constructor.js meta.group.js meta.object-literal.js
            scope = view.scope_name(region.a + 1)
            scopeArray = scope.split()
            count = len(scopeArray)
            if (count > 2 and scopeArray[count - 1] == "meta.object-literal.js" and scopeArray[count - 2] == "meta.group.js"  and scopeArray[count - 3] == "meta.function-call.constructor.js"):
                hasConstructor = True

        if (not hasCursor):
            # there might or might not be a space -> function () {} vs function (){}
            if ((leftStr == ") {" and hasParameters) or (leftNoSpacStr == "){" and hasParameters) or hasConstructor):
                inner = sublime.Region(region.a + 1, region.b - 1);
                view.fold(inner)

class FoldFunctionsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        fold(view, 0)

