import sublime, sublime_plugin

# class MyListener(sublime_plugin.EventListener):
#     openBraces = []
#     closedBraces = []
#     def on_selection_modified_async(self, view):
#         # print ("cursor", view.sel()[0])
#         braces = view.find_by_selector('meta.brace.curly.js')
#         hasUnfolded = False
        
#         self.openBraces = []
#         self.closedBraces = []

#         for brace in braces:
#             braceStr = view.substr(brace)
#             if (braceStr == "{"):
#                 self.openBraces.append(brace.a)
#             elif braceStr == "}":
#                 region = sublime.Region(self.openBraces.pop(), brace.b)
#                 self.closedBraces.append(region)

#         for brace in self.closedBraces:
#             left = sublime.Region(brace.a - 2, brace.a + 1)
#             right = sublime.Region(brace.b + 0, brace.b + 1)
#             leftStr = view.substr(left)
#             rightStr = view.substr(right)
#             if (leftStr == ") {" and (rightStr == ";" or rightStr == ",")):
#                 inner = sublime.Region(brace.a + 1, brace.b - 1);
#                 hasCursor = brace.intersects(view.sel()[0]);
#                 if hasCursor and not hasUnfolded:
#                     hasUnfolded = True
#                     view.unfold(sublime.Region(brace.a + 1, brace.b - 1))
#                 elif not hasCursor:
#                     hasUnfolded = False
#                     view.fold(inner)

class CursorListener(sublime_plugin.EventListener):
    openBraces = []
    closedBraces = []
    def on_selection_modified_async(self, view):
        # print ("cursor", view.sel()[0])
        braces = view.find_by_selector('meta.brace.curly.js')
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
        braces = view.find_by_selector('meta.brace.curly.js')
        parameters = view.find_by_selector('punctuation.definition.parameters.end.js')
        constructors = view.find_by_selector('variable.function.constructor.js')
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
            left = sublime.Region(brace.a - 2, brace.a + 1)
            leftStr = view.substr(left)
            hasCursor = brace.intersects(view.sel()[0]);
            # left of brace.a should be parameter list
            hasParameters = False
            for param in parameters:
                if left.intersects(param):
                    hasParameters = True
                    break
            # also close constructors...?
            hasConstructor = False
            for constructor in constructors:
                if left.intersects(constructor):
                    hasConstructor = True
                    break
            if (not hasCursor):
                if ((leftStr == ") {" and hasParameters) or hasConstructor):
                    inner = sublime.Region(brace.a + 1, brace.b - 1);
                    view.fold(inner)
