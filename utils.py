import re
import inflect
from syntax_rules import SYNTAX_PATTERNS

p = inflect.engine()

def normalize_word(word):
    word = word.lower().strip()

    singular = p.singular_noun(word)

    if singular:
        return singular

    return word

def remove_not_blocks(text):
    pattern = r'\{NOT.*?\}'
    return re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)

def extract_keywords(text):
    text = remove_not_blocks(text)

    tokens = re.findall(r'\b[a-zA-Z]+\b', text)

    normalized = []

    for token in tokens:
        normalized.append(normalize_word(token))

    return set(normalized)

def find_duplicate_keywords(inclusion, exclusion, exact_match=False):

    duplicates = []

    exclusion_clean = remove_not_blocks(exclusion)

    inclusion_words = extract_keywords(inclusion)

    lines = exclusion_clean.splitlines()

    for line in lines:

        words = re.findall(r'\b[a-zA-Z]+\b', line)

        normalized_line_words = [normalize_word(w) for w in words]

        for inc_word in inclusion_words:

            if exact_match:
                if inc_word in normalized_line_words:
                    duplicates.append({
                        "keyword": inc_word,
                        "matched_text": line.strip()
                    })
            else:
                for w in normalized_line_words:

                    if inc_word == w:
                        duplicates.append({
                            "keyword": inc_word,
                            "matched_text": line.strip()
                        })

    unique = []
    seen = set()

    for d in duplicates:
        key = (d['keyword'], d['matched_text'])

        if key not in seen:
            unique.append(d)
            seen.add(key)

    return unique

def detect_syntax_errors(inclusion, exclusion):

    errors = []

    combined = inclusion + "\n" + exclusion

    lines = combined.splitlines()

    for idx, line in enumerate(lines, start=1):

        if line.strip() == "":
            errors.append({
                "line": idx,
                "type": "Blank Line",
                "text": "Empty line"
            })

        for err_type, pattern in SYNTAX_PATTERNS.items():

            if re.search(pattern, line):
                errors.append({
                    "line": idx,
                    "type": err_type,
                    "text": line.strip()
                })

    return errors

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
