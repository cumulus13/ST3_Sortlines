import re
import sublime
import sublime_plugin

WS = re.compile(r'\s+')


def line_first_word(line):
    return WS.split(line.strip(), 1)[0]


def sort_text(text, reverse=False, case_sensitive=False):
    trailing = text.endswith('\n')
    if trailing:
        text = text[:-1]
    key = (lambda l: line_first_word(l)) if case_sensitive else (lambda l: line_first_word(l).lower())
    lines = sorted(text.split('\n'), key=key, reverse=reverse)  # stable
    return '\n'.join(lines) + ('\n' if trailing else '')


class SortLinesByFirstWordCommand(sublime_plugin.TextCommand):
    def run(self, edit, reverse=False, case_sensitive=False):
        v = self.view
        regions = [r for r in v.sel() if not r.empty()] or [sublime.Region(0, v.size())]
        for r in sorted(regions, key=lambda r: r.begin(), reverse=True):
            end = r.end()
            if end > r.begin() and v.rowcol(end)[1] == 0:
                end -= 1
            full = sublime.Region(v.line(r.begin()).begin(), v.line(end).end())
            v.replace(edit, full, sort_text(v.substr(full), reverse, case_sensitive))
