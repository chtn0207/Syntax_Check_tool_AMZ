import re
import inflect
from syntax_rules import SYNTAX_PATTERNS

p = inflect.engine()

# =====================================
# RESERVED WORDS
# =====================================

RESERVED_KEYWORDS = {
    "and",
    "or",
    "not"
}

# =====================================
# NORMALIZATION
# =====================================

def normalize_word(word):

    word = word.lower().strip()

    singular = p.singular_noun(word)

    if singular:
        return singular

    return word

# =====================================
# REMOVE NOT BLOCKS
# =====================================

def remove_not_blocks(text):

    pattern = r'\{NOT.*?\}'

    return re.sub(
        pattern,
        '',
        text,
        flags=re.DOTALL | re.IGNORECASE
    )

# =====================================
# REMOVE RANGE FUNCTIONS
# =====================================

def remove_range_functions(text):

    return re.sub(r':\d+:', ':', text)

# =====================================
# EXTRACT SEARCHABLE CONTENT
# =====================================

def extract_searchable_content(text):

    searchable_lines = []

    lines = text.splitlines()

    for line in lines:

        line = remove_range_functions(line)

        # Handle AttributesContain logic
        if 'AttributesContain[' in line:

            if ':' in line:
                line = line.split(':', 1)[1]
            else:
                continue

        searchable_lines.append(line)

    return '\n'.join(searchable_lines)

# =====================================
# EXTRACT KEYWORDS
# =====================================

def extract_keywords(text):

    text = remove_not_blocks(text)

    text = extract_searchable_content(text)

    tokens = re.findall(r'\b[a-zA-Z]+\b', text)

    normalized = []

    for token in tokens:

        token = normalize_word(token)

        if token not in RESERVED_KEYWORDS:
            normalized.append(token)

    return set(normalized)

# =====================================
# DUPLICATE DETECTION
# =====================================

def find_duplicate_keywords(inclusion, exclusion, exact_match=False):

    duplicates = []

    inclusion_words = extract_keywords(inclusion)

    # Use ORIGINAL exclusion lines
    original_lines = exclusion.splitlines()

    inside_not_block = False

    for line_number, original_line in enumerate(original_lines, start=1):

        line = original_line

        # ---------------------------------
        # TRACK NOT BLOCKS
        # ---------------------------------

        upper_line = line.upper()

        if '{NOT' in upper_line:
            inside_not_block = True

        if inside_not_block:

            if '}' in line:
                inside_not_block = False

            continue

        # ---------------------------------
        # REMOVE RANGE FUNCTIONS
        # ---------------------------------

        line = remove_range_functions(line)

        # ---------------------------------
        # HANDLE ATTRIBUTECONTAINS
        # ---------------------------------

        if 'AttributesContain[' in line:

            if ':' in line:
                line = line.split(':', 1)[1]
            else:
                continue

        # ---------------------------------
        # EXTRACT WORDS
        # ---------------------------------

        words = re.findall(r'\b[a-zA-Z]+\b', line)

        normalized_line_words = []

        for w in words:

            w = normalize_word(w)

            # Ignore reserved words
            if w in RESERVED_KEYWORDS:
                continue

            normalized_line_words.append(w)

        # ---------------------------------
        # COMPARE DUPLICATES
        # ---------------------------------

        for inc_word in inclusion_words:

            for w in normalized_line_words:

                if inc_word == w:

                    duplicates.append({
                        'keyword': inc_word,
                        'line_number': line_number
                    })

    # ---------------------------------
    # REMOVE DUPLICATE ENTRIES
    # ---------------------------------

    unique = []
    seen = set()

    for d in duplicates:

        key = (d['keyword'], d['line_number'])

        if key not in seen:

            unique.append(d)

            seen.add(key)

    return unique

# =====================================
# BRACE VALIDATION
# =====================================

def validate_braces(text):

    errors = []

    stack = []

    pairs = {
        '}': '{',
        ']': '['
    }

    for idx, char in enumerate(text):

        if char in ['{', '[']:
            stack.append((char, idx))

        elif char in ['}', ']']:

            if not stack:

                errors.append({
                    'type': 'Missing opening brace',
                    'position': idx
                })

            else:

                top, pos = stack.pop()

                if top != pairs[char]:

                    errors.append({
                        'type': 'Mismatched brace',
                        'position': idx
                    })

    while stack:

        top, pos = stack.pop()

        errors.append({
            'type': 'Missing closing brace',
            'position': pos
        })

    return errors

# =====================================
# SYNTAX ERROR DETECTION
# =====================================

def detect_syntax_errors(inclusion, exclusion):

    errors = []

    combined = inclusion + '\n' + exclusion

    lines = combined.splitlines()

    for idx, line in enumerate(lines, start=1):

        if line.strip() == '':

            errors.append({
                'line': idx,
                'type': 'Blank Line',
                'text': 'Empty line'
            })

        for err_type, pattern in SYNTAX_PATTERNS.items():

            if re.search(pattern, line):

                errors.append({
                    'line': idx,
                    'type': err_type,
                    'text': line.strip()
                })

    brace_errors = validate_braces(combined)

    for b in brace_errors:

        errors.append({
            'line': '-',
            'type': b['type'],
            'text': f"Position {b['position']}"
        })

    return errors

# =====================================
# HIGHLIGHT DUPLICATES
# =====================================

def highlight_text(text, duplicates):

    highlighted = text

    for dup in duplicates:

        keyword = dup['keyword']

        pattern = rf'(\b{re.escape(keyword)}(s|es)?\b)'

        highlighted = re.sub(
            pattern,
            r'<span class="duplicate">\1</span>',
            highlighted,
            flags=re.IGNORECASE
        )

    highlighted = highlighted.replace('\n', '<br>')

    return highlighted
