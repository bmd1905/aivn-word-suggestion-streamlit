
from st_keyup import st_keyup
import streamlit as st

import re
from collections import defaultdict
from operator import itemgetter

from utils import footer


st.set_page_config(page_title='AI VIETNAM', page_icon='https://scontent-ams2-1.xx.fbcdn.net/v/t39.30808-6/326762542_533351005436945_3355631653176967012_n.png?_nc_cat=1&ccb=1-7&_nc_sid=5f2048&_nc_ohc=J2pKQDyGdRgAX_FLksV&_nc_ht=scontent-ams2-1.xx&oh=00_AfDN3M3ADdj9HUK4qGIkj-F77QU6P5hja1XkdcjQQtUg2w&oe=6563863F')


@st.cache_data
def preprocess_text(text):
    # Remove punctuation and convert to lowercase
    text = re.sub(r'[^\w\s]', '', text).lower()
    return text


@st.cache_data
def create_suggestion_dict(text):
    suggestion_dict = defaultdict(list)

    text = preprocess_text(text)
    words = text.split()

    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]

        suggestion_dict[current_word].append(next_word)

    # Sort values for each key by the number of appearances
    for key in suggestion_dict:
        suggestion_dict[key] = sorted([(word, suggestion_dict[key].count(word)) for word in set(suggestion_dict[key])], key=itemgetter(1), reverse=True)

    return suggestion_dict


@st.cache_data
def load_data(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = file.read()
    return data
    
#################################################
st.title("Word Suggestions App")

# load data
with st.spinner("Loading data"):
    data = load_data('data.txt')
    
    suggestions = create_suggestion_dict(data)

# Input word and choose top-k with a slider
k = st.slider("Select the number of suggestions to show (k):", 1, 10, 5)
inputs = st_keyup("Enter text to check suggestions:", placeholder='Type something...', key='0')


# Handle input
if ' ' in inputs or inputs:
    # Process input
    inputs = inputs.strip()
    inputs = inputs.split(' ')[-1]

    # Find suggestions
    if inputs in suggestions:
        top_suggestions = suggestions[inputs][:k]
        st.success(f"{', '.join([word[0] for word in top_suggestions])}")

    else:
        st.warning(f"No suggestions found for '{inputs}'.")
        
        
#################################################
footer()
