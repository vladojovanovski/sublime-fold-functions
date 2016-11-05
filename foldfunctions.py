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

def collectBlocks (view):
    # collects function bodies
    # huge problem: find_by_selector does not find nested scopes
    bodies = view.find_by_selector('meta.block.js')
    return bodies

def fold (view, edge):
    regions = collectBlocks(view)
    closeConstructors = bool(settings.get("fold_constructors", False))
    sels = view.sel()

    for region in regions:
        # the cursor should not be here
        hasCursor = False
        for sel in sels:
            extraSel = sublime.Region(sel.a - edge, sel.a + edge)
            hasCursor = hasCursor or region.intersects(extraSel);
        if hasCursor:
            continue
        # there might be a space between the parameters and block
        innerStart = 1
        firstChar = view.substr(sublime.Region(region.a, region.a + 1))
        if firstChar == " ":
            innerStart = 2
        # fold the inner part without the braces
        inner = sublime.Region(region.a + innerStart, region.b - 1);
        view.fold(inner)

class FoldFunctionsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        fold(view, 0)

