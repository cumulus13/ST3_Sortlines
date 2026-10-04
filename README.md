# SortLines (Sublime Text 3)

Sorts lines inside the current file (or only the selection) by the first word of each line.
Ctrl+Shift+P -> "Sort Lines: First Word ..." (A-Z / Z-A, case-sensitive / case-insensitive).

Command: sort_lines_by_first_word  args: reverse, case_sensitive
Install: copy SortLines.sublime-package to Data/Installed Packages/

## Duplicate marking
Ctrl+Shift+P -> "Duplicates: ..."  (mark_duplicate_lines / clear_duplicate_marks)
Args: case_sensitive (false), strip (true), mark_first (true), ignore_blank (true).
Color: SortLines.sublime-settings -> duplicate_background (default #FFFF00).
Marks do not follow edits reliably; re-run or clear after changing the file.

## Key bindings (Windows/Linux/OSX, all Ctrl+Alt+Shift+...)
A = sort A-Z, Z = sort Z-A (case-insensitive); Q / W = A-Z / Z-A case-sensitive
D = mark duplicates (case-insens.), E = mark duplicates (case-sens.), C = clear marks
Edit via Preferences > Key Bindings if any conflicts with your own keys.

## 👤 Author
        
[Hadi Cahyadi](mailto:cumulus13@gmail.com)
    

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)
 
[Support me on Patreon](https://www.patreon.com/cumulus13)
