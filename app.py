import streamlit as st
from utils import (
    find_duplicate_keywords,
    detect_syntax_errors,
    highlight_text,
)

st.set_page_config(
    page_title="Syntax Error Detection Tool",
    layout="wide"
)

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Syntax Error Detection Tool")
st.markdown("### Inclusion & Exclusion Validation Engine")

col1, col2 = st.columns(2)

with col1:
    inclusion_text = st.text_area(
        "Keywords to Include",
        height=500,
        placeholder="Paste inclusion syntax here..."
    )

with col2:
    exclusion_text = st.text_area(
        "Keywords to Exclude",
        height=500,
        placeholder="Paste exclusion syntax here..."
    )

exact_match = st.checkbox("Exact Match Only")

if st.button("Check Syntax"):

    duplicates = find_duplicate_keywords(
        inclusion_text,
        exclusion_text,
        exact_match=exact_match
    )

    syntax_errors = detect_syntax_errors(
        inclusion_text,
        exclusion_text
    )

    st.subheader("Duplicate Keyword Errors")

    if duplicates:
        for dup in duplicates:
            st.error(
                f"Duplicate keyword found: {dup['keyword']} → {dup['matched_text']}"
            )
    else:
        st.success("No duplicate keyword errors found")

    st.subheader("Syntax Errors")

    if syntax_errors:
        for err in syntax_errors:
            st.warning(
                f"Line {err['line']} → {err['type']} → {err['text']}"
            )
    else:
        st.success("No syntax errors found")

    st.subheader("Highlighted Exclusion Syntax")

    highlighted = highlight_text(exclusion_text, duplicates)

    st.markdown(
        f'<div class="highlight-box">{highlighted}</div>',
        unsafe_allow_html=True
    )
