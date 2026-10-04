import json
import os
import sublime
import sublime_plugin

KEY = "sortlines_duplicates"
SCOPE = "sortlines.duplicate"
FALLBACK_SCOPE = "region.yellowish"   # used when build < 3149 (no .sublime-color-scheme)
COLOR_PKG = "SortLinesColors"
SETTINGS = "SortLines.sublime-settings"


def find_duplicate_indices(lines, case_sensitive=False, strip=True,
                           mark_first=True, ignore_blank=True):
    """Return sorted list of line indices that are duplicates."""
    def norm(s):
        if strip:
            s = s.strip()
        return s if case_sensitive else s.lower()

    groups = {}
    for i, l in enumerate(lines):
        k = norm(l)
        if ignore_blank and not k.strip():
            continue
        groups.setdefault(k, []).append(i)

    out = []
    for idxs in groups.values():
        if len(idxs) > 1:
            out.extend(idxs if mark_first else idxs[1:])
    return sorted(out)


def _scheme_stem(view):
    cs = view.settings().get("color_scheme") or ""
    base = os.path.basename(cs)
    for ext in (".sublime-color-scheme", ".tmTheme"):
        if base.endswith(ext):
            return base[:-len(ext)]
    return base or None


def _ensure_scheme(view, color):
    """Write an override color scheme (rules only) for the active scheme.
    Returns the scope to use."""
    try:
        if int(sublime.version()) < 3149:
            return FALLBACK_SCOPE
        stem = _scheme_stem(view)
        if not stem:
            return FALLBACK_SCOPE
        folder = os.path.join(sublime.packages_path(), COLOR_PKG)
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, stem + ".sublime-color-scheme")
        data = {"rules": [{"scope": SCOPE, "background": color, "foreground": "#000000"}]}
        text = json.dumps(data, indent=4)
        old = None
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                old = f.read()
        if old != text:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        return SCOPE
    except Exception as e:
        print("SortLines: color scheme setup failed:", e)
        return FALLBACK_SCOPE


class MarkDuplicateLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit, case_sensitive=False, strip=True, mark_first=True,
            ignore_blank=True):
        v = self.view
        color = sublime.load_settings(SETTINGS).get("duplicate_background", "#FFFF00")

        sel = [r for r in v.sel() if not r.empty()]
        if sel:
            line_regions = []
            for r in sel:
                line_regions.extend(v.split_by_newlines(v.line(r.begin()).cover(v.line(r.end()))))
        else:
            line_regions = v.split_by_newlines(sublime.Region(0, v.size()))

        lines = [v.substr(r) for r in line_regions]
        idx = find_duplicate_indices(lines, case_sensitive, strip, mark_first, ignore_blank)
        regions = [line_regions[i] for i in idx]

        scope = _ensure_scheme(v, color)
        v.erase_regions(KEY)
        if regions:
            v.add_regions(KEY, regions, scope, "", sublime.DRAW_NO_OUTLINE)
        sublime.status_message("SortLines: %d duplicate line(s) marked" % len(regions))


class ClearDuplicateMarksCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.erase_regions(KEY)
        sublime.status_message("SortLines: duplicate marks cleared")
