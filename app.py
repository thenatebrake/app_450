import streamlit as st
import pandas as pd

from game import (
    SpellingGame,
    generate_valid_words,
    score_word,
    get_level
)

from dictionary import Dictionary
from puzzle import PUZZLE


# --------------------------
# Setup
# --------------------------

dictionary = Dictionary()

valid_words = generate_valid_words(
    dictionary.words,
    PUZZLE["letters"],
    PUZZLE["center"]
)

max_score = sum(
    score_word(word, PUZZLE)
    for word in valid_words
)


# --------------------------
# Session state
# --------------------------

if "found_words" not in st.session_state:
    st.session_state.found_words = set()

if "score" not in st.session_state:
    st.session_state.score = 0

if "current_word" not in st.session_state:
    st.session_state.current_word = ""


# --------------------------
# Tabs
# --------------------------

play_tab, analysis_tab = st.tabs([
    "🐝 Play",
    "📊 Puzzle Analysis"
])


# ==================================================
# PLAY
# ==================================================

with play_tab:

    st.title("HiveWords")

    score = st.session_state.score

    level = get_level(
        score,
        max_score
    )

    st.metric(
        "Score",
        score
    )

    st.write(f"### {level}")

    st.progress(
        min(score / max_score, 1.0)
    )

    st.write(
        f"{len(st.session_state.found_words)} "
        f"/ {len(valid_words)} words"
    )

    # Your existing hive UI goes here

    # Your existing input/submission UI goes here


# ==================================================
# ANALYSIS
# ==================================================

with analysis_tab:

    st.title("Puzzle Analysis")

    st.write(
        f"**{len(valid_words)} possible words**"
    )

    st.write(
        f"**{max_score} possible points**"
    )

    # Word distribution
    distribution = {}

    for word in valid_words:

        letter = word[0]
        length = len(word)

        if letter not in distribution:
            distribution[letter] = {}

        if length not in distribution[letter]:
            distribution[letter][length] = 0

        distribution[letter][length] += 1

    rows = []

    for letter in sorted(distribution):

        for length in sorted(distribution[letter]):

            rows.append({
                "Starting Letter": letter,
                "Length": length,
                "Words": distribution[letter][length]
            })

    df = pd.DataFrame(rows)

    st.subheader(
        "Word Length Distribution"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    # First two letters

    from collections import Counter

    combinations = Counter(
        word[:2]
        for word in valid_words
    )

    combo_rows = [
        {
            "Combination": combo,
            "Words": count
        }
        for combo, count
        in combinations.most_common()
    ]

    combo_df = pd.DataFrame(combo_rows)

    st.subheader(
        "First Two Letter Combinations"
    )

    st.dataframe(
        combo_df,
        use_container_width=True,
        hide_index=True
    )