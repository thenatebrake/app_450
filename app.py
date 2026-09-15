import streamlit as st

from game import SpellingGame
from dictionary import Dictionary
from puzzle import PUZZLE


# -------------------------
# Page configuration
# -------------------------

st.set_page_config(
    page_title="HiveWords",
    page_icon="🐝",
    layout="centered"
)


# -------------------------
# Initialize game
# -------------------------

if "found_words" not in st.session_state:
    st.session_state.found_words = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "current_word" not in st.session_state:
    st.session_state.current_word = ""


dictionary = Dictionary()

game = SpellingGame(
    PUZZLE["letters"],
    PUZZLE["center"],
    dictionary
)


# -------------------------
# Header
# -------------------------

st.title("🐝 HiveWords")

st.write("Find words using the letters below.")


# -------------------------
# Score
# -------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Score",
        st.session_state.score
    )

with col2:
    st.metric(
        "Words",
        len(st.session_state.found_words)
    )


# -------------------------
# Hive
# -------------------------

st.subheader("Letters")


letters = list(PUZZLE["letters"])

# Sort so layout is predictable
letters.sort()

center = PUZZLE["center"]

outer_letters = [
    letter for letter in letters
    if letter != center
]


# Top
st.markdown(
    f"""
    <div style="text-align:center; font-size:40px;">
        {outer_letters[0]}
    </div>
    """,
    unsafe_allow_html=True
)


# Middle
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"<div style='text-align:center;font-size:40px'>{outer_letters[1]}</div>",
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
        f"<div style='text-align:center;font-size:40px'>{outer_letters[2]}</div>",
        unsafe_allow_html=True
    )


# Bottom
st.markdown(
    f"""
    <div style="text-align:center; font-size:40px;">
        {outer_letters[3]}
    </div>
    """,
    unsafe_allow_html=True
)


# -------------------------
# Word input
# -------------------------

word = st.text_input(
    "Enter a word",
    key="word_input"
)


# -------------------------
# Submit
# -------------------------

if st.button("Submit", use_container_width=True):

    valid, message = game.validate_word(word)

    if not valid:
        st.error(message)

    elif word.upper() in st.session_state.found_words:
        st.warning("You already found that word.")

    else:
        word = word.upper()

        points = game.score_word(word)

        st.session_state.found_words.append(word)
        st.session_state.score += points

        st.success(
            f"{word} +{points} points!"
        )

        # Clear input
        st.session_state.word_input = ""


# -------------------------
# Found words
# -------------------------

st.divider()

st.subheader("Found Words")

if st.session_state.found_words:

    for word in sorted(
        st.session_state.found_words,
        key=lambda x: (len(x), x)
    ):
        st.write(word)

else:
    st.write("No words found yet.")