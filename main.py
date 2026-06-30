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
            words_data = pd.read_csv("data/french_words.csv")
        except FileNotFoundError:
            st.error("Error: Could not find data/french_words.csv. Please make sure the data folder is uploaded to GitHub!")
            st.stop()
            
    st.session_state.words_data_list = words_data.to_dict(orient="records")

# 2. Pick a random word if we don't have one
if 'current_word' not in st.session_state:
    st.session_state.current_word = random.choice(st.session_state.words_data_list)

# 3. Keep track of whether the card is showing front (False) or back (True)
if 'is_flipped' not in st.session_state:
    st.session_state.is_flipped = False


# --- Button Logic Functions ---
def flip_card():
    st.session_state.is_flipped = True

def next_card():
    # Pick a new word and flip the card back to the front
    st.session_state.current_word = random.choice(st.session_state.words_data_list)
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
st.title("📇 Flashy - Language Learning")

# Display the card based on whether it is flipped or not
if not st.session_state.is_flipped:
    # FRONT OF CARD (French)
    st.markdown(f"""
        <div class="flashcard">
            <div class="language-text">French</div>
            <div class="word-text">{st.session_state.current_word['French']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Button to flip
    st.button("🔄 Flip Card", on_click=flip_card, use_container_width=True)

else:
    # BACK OF CARD (English)
    st.markdown(f"""
        <div class="flashcard" style="background-color: #91c2af; color: white;">
            <div class="language-text" style="color: white;">English</div>
            <div class="word-text" style="color: white;">{st.session_state.current_word['English']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Display the Right/Wrong buttons side by side
    col1, col2 = st.columns(2)
    with col1:
        st.button("❌ I don't know it", on_click=next_card, use_container_width=True)
    with col2:
        st.button("✅ I know it", on_click=is_known, use_container_width=True)

# Show progress at the bottom
st.caption(f"Words remaining to learn: {len(st.session_state.words_data_list)}")from tkinter import *

import pandas
import random

# words data
try:
    words_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    words_data = pandas.read_csv("data/french_words.csv")
words_data_list = words_data.to_dict(orient="records")

BACKGROUND_COLOR = "#B1DDC6"

shown_word = {}


def is_unknown():
    """Shows the next word on the card."""
    global shown_word, flip_timer
    window.after_cancel(flip_timer)
    # try:
    shown_word = random.choice(words_data_list)
    # except IndexError:
    #     messagebox.showinfo(title="We are finished.", message="You have learned all of the words in this application.")
    # else:
    canvas.itemconfig(bg_image, image=card_front)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=shown_word["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def is_known():
    global shown_word
    words_data_list.remove(shown_word)
    data = pandas.DataFrame(words_data_list)
    data.to_csv("data/words_to_learn.csv", index=False)
    is_unknown()
    print(len(data))
    # try:
    # except ValueError, IndexError:
    # else:


def flip_card():
    global shown_word
    canvas.itemconfig(bg_image, image=card_back)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=shown_word["English"], fill="white")


# window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

# card front
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
bg_image = canvas.create_image(400, 263, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)

# text
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

# buttons
wrong_button_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=is_unknown)
wrong_button.grid(row=1, column=0)

right_button_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_button_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

is_unknown()

window.mainloop()
