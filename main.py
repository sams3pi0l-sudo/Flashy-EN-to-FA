import streamlit as st
import pandas as pd
import random
import os

# --- Page Configuration ---
# This changes the browser tab title and sets the page layout
st.set_page_config(page_title="Flashy", page_icon="📇", layout="centered")

# --- Custom CSS ---
# We use HTML/CSS to recreate the beautiful Tkinter Canvas look natively for the web
BACKGROUND_COLOR = "#B1DDC6"
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {BACKGROUND_COLOR};
    }}
    .flashcard {{
        background-color: white;
        border-radius: 20px;
        padding: 60px;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }}
    .language-text {{
        font-size: 30px;
        font-style: italic;
        color: #333333;
        margin-bottom: 10px;
    }}
    .word-text {{
        font-size: 60px;
        font-weight: bold;
        color: #000000;
    }}
    </style>
""", unsafe_allow_html=True)

# --- State Management (Memory) ---
# Because Streamlit reruns on every click, we must save our data in session_state

# 1. Load data only once
if 'words_data_list' not in st.session_state:
    try:
        words_data = pd.read_csv("data/words_to_learn.csv")
    except FileNotFoundError:
        # Fallback if words_to_learn doesn't exist
        try:
            words_data = pd.read_csv("data/english_words.csv")
        except FileNotFoundError:
            st.error("Error: Could not find data/french_words.csv. Please make sure the data folder is uploaded to GitHub!")
            st.stop()
            
    st.session_state.words_data_list = words_data.to_dict(orient="records")

# 2. Pick a random word if we don't have one
if 'current_word' not in st.session_state:
    if len(st.session_state.words_data_list) > 0:
        st.session_state.current_word = random.choice(st.session_state.words_data_list)
    else:
        st.session_state.current_word = None
    st.session_state.current_word = random.choice(st.session_state.words_data_list)

# 3. Keep track of whether the card is showing front (False) or back (True)
if 'is_flipped' not in st.session_state:
    st.session_state.is_flipped = False


# --- Button Logic Functions ---
def flip_card():
    st.session_state.is_flipped = True

def next_card():
    # Pick a new word and flip the card back to the front
    if len(st.session_state.words_data_list) > 0:
        st.session_state.current_word = random.choice(st.session_state.words_data_list)
    else:
        st.session_state.current_word = None
    st.session_state.is_flipped = False

def is_known():
    # Remove the word from the list
    st.session_state.words_data_list.remove(st.session_state.current_word)
    
    # Save the updated list to the CSV
    data = pd.DataFrame(st.session_state.words_data_list)
    # Ensure the data directory exists before saving
    os.makedirs('data', exist_ok=True)
    data.to_csv("data/words_to_learn.csv", index=False)
    
    # Move to the next card
    next_card()


# --- User Interface ---
st.title("📇 Flashy - For You My Precious❤️")

if len(st.session_state.words_data_list) == 0 or st.session_state.current_word is None:
    st.success("🎉 Congratulations! You have learned all the words!")
    st.balloons() # This triggers a nice celebration animation!
    st.stop()     # This safely stops rendering the rest of the page

# Display the card based on whether it is flipped or not
if not st.session_state.is_flipped:
    # FRONT OF CARD (English)
    st.markdown(f"""
        <div class="flashcard">
            <div class="language-text">English</div>
            <div class="word-text">{st.session_state.current_word['English']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Button to flip
    st.button("🔄 Flip Card", on_click=flip_card, use_container_width=True)

else:
    # BACK OF CARD (Persian)
    st.markdown(f"""
        <div class="flashcard" style="background-color: #91c2af; color: white;">
            <div class="language-text" style="color: white;">Persian</div>
            <div class="word-text" style="color: white;">{st.session_state.current_word['Persian']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Display the Right/Wrong buttons side by side
    col1, col2 = st.columns(2)
    with col1:
        st.button("❌ I don't know it", on_click=next_card, use_container_width=True)
    with col2:
        st.button("✅ I know it", on_click=is_known, use_container_width=True)

# Show progress at the bottom
st.caption(f"Words remaining to learn: {len(st.session_state.words_data_list)}")
