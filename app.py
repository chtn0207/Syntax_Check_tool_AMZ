import streamlit as st

from utils import (
    find_duplicate_keywords,
    detect_syntax_errors,
    highlight_text,
)

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Syntax Error Detection Tool",
    layout="wide"
)

# =====================================
# LOAD CSS
# =====================================

with open("styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# =====================================
# HEADER
# =====================================

st.title("Syntax Error Detection Tool")

st.markdown(
    "### Inclusion & Exclusion Validation Engine"
)

# =====================================
# INPUT COLUMNS
# =====================================

col1, col2 = st.columns(2)

with col1:

    inclusion_text = st.text_area(
        "Keywords to Include",
        height=500,
        placeholder="Paste inclusion syntax here...",
        label_visibility="visible"
    )

with col2:

    exclusion_text = st.text_area(
        "Keywords to Exclude",
        height=500,
        placeholder="Paste exclusion syntax here...",
        label_visibility="visible"
    )

# =====================================
# OPTIONS
# =====================================

exact_match = st.checkbox("Exact Match Only")

# =====================================
# BUTTON ACTION
# =====================================

if st.button("Check Syntax"):

    # ---------------------------------
    # FIND DUPLICATES
    # ---------------------------------

    duplicates = find_duplicate_keywords(
        inclusion_text,
        exclusion_text,
        exact_match=exact_match
    )

    # ---------------------------------
    # FIND SYNTAX ERRORS
    # ---------------------------------

    syntax_errors = detect_syntax_errors(
        inclusion_text,
        exclusion_text
    )

    # =================================
    # DUPLICATE OUTPUT
    # =================================

    st.subheader("Duplicate Keyword Errors")

    if duplicates:

        shown = set()

        for dup in duplicates:

            key = (
                dup['keyword'],
                dup['line_number']
            )

            if key not in shown:

                st.error(
                    f"Duplicate keyword found: "
                    f"{dup['keyword']} → "
                    f"Line {dup['line_number']}"
                )

                shown.add(key)

    else:

        st.success(
            "No duplicate keyword errors found"
        )

    # =================================
    # SYNTAX ERRORS OUTPUT
    # =================================

    st.subheader("Syntax Errors")

    if syntax_errors:

        for err in syntax_errors:

            st.warning(
                f"Line {err['line']} → "
                f"{err['type']} → "
                f"{err['text']}"
            )

    else:

        st.success(
            "No syntax errors found"
        )

    # =================================
    # HIGHLIGHTED EXCLUSION VIEW
    # =================================

    st.subheader("Highlighted Exclusion Syntax")

    highlighted = highlight_text(
        exclusion_text,
        duplicates
    )

    st.markdown(
        f'<div class="highlight-box">{highlighted}</div>',
        unsafe_allow_html=True
    )
