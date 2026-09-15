import streamlit as st
import pandas as pd
from collections import Counter

from game import (
    SpellingGame,
    generate_valid_words,
    score_word,
    get_level,
    is_queen_bee
)

from dictionary import Dictionary
from puzzle import PUZZLE


# --------------------------
# Page configuration
# --------------------------

st.set_page_config(
    page_title="HiveWords",
    page_icon="🐝",
    layout="centered"
)


# --------------------------
# Load dictionary
# --------------------------

dictionary = Dictionary()


# --------------------------
# Generate all valid words
# --------------------------

@st.cache_data
def get_valid_words(words, letters, center):
    return generate_valid_words(
        words,
        letters,
        center
    )


valid_words = get_valid_words(
    dictionary.words,
    PUZZLE["letters"],
    PUZZLE["center"]
)


# --------------------------
# Calculate maximum score
# --------------------------

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
# Game
# --------------------------

game = SpellingGame(
    PUZZLE["letters"],
    PUZZLE["center"],
    dictionary
)


# --------------------------
# Tabs
# --------------------------

play_tab, analysis_tab = st.tabs([
    "🐝 Play",
    "📊 Puzzle Analysis"
])


# ==================================================
# PLAY TAB
# ==================================================

with play_tab:

    st.title("HiveWords")

    st.write(
        "Find words using the letters below."
    )

    # --------------------------
    # Score information
    # --------------------------

    score = st.session_state.score

    level = get_level(
        score,
        max_score
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Score",
            score
        )

    with col2:
        st.metric(
            "Words",
            len(st.session_state.found_words)
        )

    with col3:
        st.metric(
            "Possible",
            len(valid_words)
        )

    st.subheader(level)

    if max_score > 0:
        st.progress(
            min(score / max_score, 1.0)
        )

    st.write(
        f"{score} / {max_score} possible points"
    )

    st.write(
        f"{len(st.session_state.found_words)} "
        f"/ {len(valid_words)} words found"
    )


    # --------------------------
    # Hive
    # --------------------------

    st.subheader("Letters")

    letters = sorted(PUZZLE["letters"])
    center = PUZZLE["center"]

    outer_letters = [
        letter
        for letter in letters
        if letter != center
    ]


    # Top letter

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:40px;
            font-weight:bold;
            margin-bottom:10px;
        ">
            {outer_letters[0]}
        </div>
        """,
        unsafe_allow_html=True
    )


    # Middle row

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:40px;
                font-weight:bold;
            ">
                {outer_letters[1]}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:40px;
                font-weight:bold;
            ">
                {center}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:40px;
                font-weight:bold;
            ">
                {outer_letters[2]}
            </div>
            """,
            unsafe_allow_html=True
        )


    # Bottom row

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:40px;
            font-weight:bold;
            margin-top:10px;
        ">
            {outer_letters[3]}
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------
    # Word input
    # --------------------------

    word = st.text_input(
        "Enter a word",
        key="word_input"
    )


    # --------------------------
    # Submit
    # --------------------------

    if st.button(
        "Submit",
        use_container_width=True
    ):

        word = word.upper().strip()

        if word in st.session_state.found_words:

            st.warning(
                "You already found that word."
            )

        else:

            valid, message = game.validate_word(word)

            if not valid:

                st.error(message)

            else:

                points = game.score_word(word)

                st.session_state.found_words.add(word)
                st.session_state.score += points

                st.success(
                    f"{word} +{points} points!"
                )

                if is_queen_bee(
                    st.session_state.found_words,
                    valid_words
                ):
                    st.balloons()

                    st.success(
                        "🐝 QUEEN BEE! "
                        "You found every possible word!"
                    )


    # --------------------------
    # Found words
    # --------------------------

    st.divider()

    st.subheader("Found Words")

    if st.session_state.found_words:

        sorted_words = sorted(
            st.session_state.found_words,
            key=lambda x: (len(x), x)
        )

        for word in sorted_words:

            points = game.score_word(word)

            st.write(
                f"**{word}** — {points} points"
            )

    else:

        st.write(
            "No words found yet."
        )


# ==================================================
# ANALYSIS TAB
# ==================================================

with analysis_tab:

    st.title("Puzzle Analysis")

    st.write(
        "Statistics for all possible words in this puzzle."
    )


    # --------------------------
    # Summary
    # --------------------------

    pangrams = [
        word
        for word in valid_words
        if set(word) == set(PUZZLE["letters"])
    ]

    average_length = (
        sum(len(word) for word in valid_words)
        / len(valid_words)
        if valid_words
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Possible Words",
            len(valid_words)
        )

    with col2:
        st.metric(
            "Maximum Score",
            max_score
        )

    with col3:
        st.metric(
            "Pangrams",
            len(pangrams)
        )

    with col4:
        st.metric(
            "Avg. Length",
            f"{average_length:.1f}"
        )


    # --------------------------
    # Word length distribution
    # --------------------------

    st.divider()

    st.subheader(
        "Word Length Distribution by Starting Letter"
    )

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

        for length in sorted(
            distribution[letter]
        ):

            rows.append({
                "Starting Letter": letter,
                "Word Length": length,
                "Number of Words":
                    distribution[letter][length]
            })


    if rows:

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


    # --------------------------
    # First two combinations
    # --------------------------

    st.divider()

    st.subheader(
        "First Two Letter Combinations"
    )

    combinations = Counter(
        word[:2]
        for word in valid_words
    )

    combo_rows = [
        {
            "Combination": combo,
            "Number of Words": count
        }
        for combo, count
        in combinations.most_common()
    ]


    if combo_rows:

        combo_df = pd.DataFrame(
            combo_rows
        )

        st.dataframe(
            combo_df,
            use_container_width=True,
            hide_index=True
        )


    # --------------------------
    # Pangrams
    # --------------------------

    st.divider()

    st.subheader("Pangrams")

    if pangrams:

        for word in sorted(pangrams):

            st.write(word)

    else:

        st.write(
            "No pangrams in this puzzle."
        )