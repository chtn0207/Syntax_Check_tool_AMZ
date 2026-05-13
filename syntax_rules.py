SYNTAX_PATTERNS = {

    "Double space before ]": r'\s{2,}\]',

    "Double space before |": r'\s{2,}\|',

    "Space after pipe": r'\|\s+',

    "Space before pipe": r'\s+\|',

    "Empty pipeline": r'\|\s*\|',

    "Invalid colon pattern": r'\[\|\s*:\|',

    "Pipe followed by colon": r'\|:',

    "Invalid dot pipeline": r'\|\.\|',

    "Invalid [.] token": r'\|\[\.\]\|',

    "Double spaces before }": r'\]\s{2,}\}',

    "Space after }": r'\}\s+',

    "Multiple consecutive spaces": r'\s{2,}',

    "Dot with spaces": r'\|\.\s{2,}\.\|',

    "Space before colon": r'\s\.:',

    "Space after colon": r':\.\s',

    "Space before ]": r'\s\.\]',

    "Leading pipe spacing": r'\|\s+[a-zA-Z]',

    "Trailing pipe spacing": r'[a-zA-Z]\s+\|'
}
